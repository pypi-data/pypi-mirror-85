use cpython::exc::{TypeError, ValueError};
use cpython::{
    ObjectProtocol, PyBytes, PyClone, PyErr, PyIterator, PyObject, PyResult, PyTuple, Python,
    PythonObject, PythonObjectDowncastError,
};
use log::{debug, error};
use python3_sys::PyObject_GetIter;
use std::io;
use std::sync::Arc;

use crate::filewrapper::{FileWrapper, SendFile};
use crate::globals::WSGIGlobals;
use crate::pyutils::{close_pyobject, PyGILState_STATE};
use crate::request::WSGIRequest;
use crate::startresponse::{StartResponse, WriteResponse};
use crate::transport::Write;

pub const HTTP500: &[u8] = b"HTTP/1.1 500 Internal Server Error\r\n\r\n";
pub const HTTP400: &[u8] = b"HTTP/1.1 400 Bad Request\r\n\r\n";

fn wsgi_iterable(obj: PyObject, py: Python) -> Result<PyObject, PythonObjectDowncastError> {
    unsafe {
        let ptr = PyObject_GetIter(obj.as_ptr());
        // Returns NULL if an object cannot be iterated.
        if ptr.is_null() {
            PyErr::fetch(py);
            return Err(PythonObjectDowncastError::new(
                py,
                "iterable",
                obj.get_type(py),
            ));
        }
        Ok(PyObject::from_owned_ptr(py, ptr))
    }
}

pub struct WSGIResponse {
    pub pyobject: Option<PyObject>,
    pub iterable: Option<PyObject>,
    pub start_response: Option<PyObject>,
    // flag indicating whether either this is the last chunk of the wsgi iterable or
    // we are using a file wrapper + sendfile and the file has been sent completely
    // (assuming no iterable in the file wrapper case)
    pub last_chunk_or_file_sent: bool,
    pub sendfileinfo: bool,
    pub current_chunk: Vec<u8>,
    pub content_length: Option<usize>,
    pub written: usize,
}

impl WSGIResponse {
    pub fn new() -> WSGIResponse {
        WSGIResponse {
            pyobject: None,
            iterable: None,
            start_response: None,
            last_chunk_or_file_sent: false,
            sendfileinfo: false,
            current_chunk: Vec::new(),
            content_length: None,
            written: 0,
        }
    }

    pub fn set_pyobject(&mut self, pyobject: PyObject, py: Python) {
        let iterable = match wsgi_iterable(pyobject.clone_ref(py), py) {
            Ok(pyiter) => Some(pyiter),
            Err(e) => {
                debug!("Could not create iterator: {:?}", e);
                None
            }
        };
        self.iterable = iterable;
        if let Ok(fw) = pyobject.extract::<&FileWrapper>(py) {
            if fw.sendfileinfo(py).borrow().fd != -1 {
                self.sendfileinfo = true;
            }
        }
        self.pyobject = Some(pyobject);
    }

    fn set_error_500(&mut self) {
        self.current_chunk = HTTP500.to_vec();
        self.last_chunk_or_file_sent = true;
    }

    fn set_bad_request_400(&mut self) {
        self.current_chunk = HTTP400.to_vec();
        self.last_chunk_or_file_sent = true;
    }

    // true: There's more. false: done
    pub fn render_next_chunk(&mut self, py: Python) -> PyResult<()> {
        match self.start_response.as_mut() {
            Some(pyob) => {
                let mut start_response = pyob.extract::<StartResponse>(py)?;
                match self.iterable.as_mut() {
                    None => {
                        // handle FileWrapper here
                        if let Some(ob) = self.pyobject.as_mut() {
                            match ob.extract::<FileWrapper>(py) {
                                Ok(mut fw) => match fw.next() {
                                    Some(cont) => {
                                        start_response.write(&cont, &mut self.current_chunk, py);
                                        if self.sendfileinfo & self.content_length.is_none() {
                                            self.content_length = start_response.content_length(py);
                                        }
                                    }
                                    None => {
                                        self.last_chunk_or_file_sent = true;
                                        match close_pyobject(ob, py) {
                                            Err(e) => e.print_and_set_sys_last_vars(py),
                                            Ok(_) => debug!("WSGIResponse dropped successfully"),
                                        }
                                        return Ok(());
                                    }
                                },
                                Err(err) => {
                                    // No iterator, no FileWrapper, there's nothing we can do
                                    debug!("Could not extract FileWrapper: {:?}", err);
                                    PyErr::fetch(py);
                                    self.last_chunk_or_file_sent = true;
                                    return Ok(());
                                }
                            }
                        }
                    }
                    Some(obj) => match PyIterator::from_object(py, obj.clone_ref(py)) {
                        Ok(mut iter) => match iter.next() {
                            None => {
                                self.last_chunk_or_file_sent = true;
                                return Ok(());
                            }
                            Some(Err(e)) => return Err(e),
                            Some(Ok(any)) => match any.cast_as::<PyBytes>(py) {
                                Ok(cont) => {
                                    start_response.write(
                                        cont.data(py),
                                        &mut self.current_chunk,
                                        py,
                                    );
                                }
                                Err(e) => {
                                    error!(
                                        "Could not downcast from: {:?}, got error: {:?}",
                                        any, e
                                    );
                                    self.last_chunk_or_file_sent = true;
                                    return Ok(());
                                }
                            },
                        },
                        Err(_) => {
                            return Err(PyErr::new::<TypeError, _>(
                                py,
                                format!("Could not create iterator from {:?}", obj),
                            ))
                        }
                    },
                }
                if start_response.content_complete(py) {
                    debug!("start_response content complete");
                    self.last_chunk_or_file_sent = true;
                }
                Ok(())
            }
            None => Err(PyErr::new::<ValueError, _>(py, "StartResponse not set")),
        }
    }

    // true: chunk written completely, false: there's more
    pub fn write_chunk<T: Write>(
        &mut self,
        out: &mut T,
        py: Python,
        gstate: PyGILState_STATE,
    ) -> io::Result<bool> {
        let mut chunk_complete = false;
        if !self.last_chunk_or_file_sent & (self.written == 0) {
            debug!("Attempt to render next chunk");
            if let Err(e) = self.render_next_chunk(py) {
                error!("Could not render WSGI chunk: {:?}", e);
                PyErr::fetch(py);
                self.set_error_500();
            }
        }
        match out.write(&self.current_chunk[self.written..]) {
            Ok(n) => {
                self.written += n;
                debug!("{} bytes written", self.written);
                if self.written == self.current_chunk.len() {
                    chunk_complete = true;
                    debug!("done writing");
                    if !self.last_chunk_or_file_sent {
                        self.current_chunk.clear();
                        self.written = 0;
                    }
                }
            }
            Err(err) => return Err(err),
        }
        if self.sendfileinfo {
            if let Some(ob) = self.pyobject.as_mut() {
                self.last_chunk_or_file_sent = match ob.extract::<FileWrapper>(py) {
                    Ok(mut fw) => {
                        debug!("self.content_length: {:?}", self.content_length);
                        if let Some(cl) = self.content_length {
                            fw.update_content_length(cl, py);
                        }
                        fw.send_file(out, gstate, py)
                    }
                    Err(_) => {
                        // No iterator, no FileWrapper, there's nothing we can do here
                        debug!("Could not extract FileWrapper");
                        PyErr::fetch(py);
                        true
                    }
                }
            }
        }
        out.flush()?;
        debug!(
            "write_chunk last_chunk: {} chunk_complete: {}",
            self.last_chunk_or_file_sent, chunk_complete
        );
        Ok(chunk_complete && self.last_chunk_or_file_sent)
    }

    pub fn complete(&self) -> bool {
        // needed in case of EAGAIN error
        self.last_chunk_or_file_sent && (self.written == 0)
    }
}

pub fn handle_request(
    application: &PyObject,
    globals: &WSGIGlobals,
    req: &mut WSGIRequest,
    py: Python,
) {
    let mut resp = WSGIResponse::new();
    // no need to proceed if we have a bad request
    if req.is_bad_request() {
        resp.set_bad_request_400();
    } else {
        match req.wsgi_environ(globals, py) {
            Ok(env) => {
                // allocate the Python object on the heap
                match StartResponse::new(env, Vec::new(), py) {
                    Ok(sr) => {
                        let envarg = sr.environ(py).into_object();
                        let args = PyTuple::new(py, &[envarg, sr.as_object().clone_ref(py)]);
                        let srobj = sr.into_object();
                        debug!(
                            "Refcounts application: {:?} start_response: {:?}",
                            application.get_refcnt(py),
                            srobj.get_refcnt(py),
                        );
                        resp.start_response = Some(srobj);
                        let result = application.call(py, args, None); // call the object
                        match result {
                            Ok(o) => {
                                debug!("Refcount result: {:?}", o.get_refcnt(py));
                                resp.set_pyobject(o, py);
                            }
                            Err(e) => {
                                e.print_and_set_sys_last_vars(py);
                                resp.set_error_500();
                            }
                        }
                    }
                    Err(e) => {
                        error!("Error creating start_response: {:?}", e);
                        resp.set_error_500();
                    }
                }
            }
            Err(e) => {
                error!("Error handling request: {:?}", e);
                e.print_and_set_sys_last_vars(py);
                resp.set_error_500();
            }
        }
    }
    req.response = Arc::new(Some(resp));
}

#[cfg(test)]
mod tests {

    use cpython::exc::TypeError;
    use cpython::{PyClone, PyDict, Python, PythonObject};
    use log::debug;
    use mio::net::TcpStream;
    use std::io::{Read, Seek, Write};
    use std::net::{SocketAddr, TcpListener};
    use std::os::unix::io::AsRawFd;
    use std::sync::mpsc::channel;
    use std::sync::Arc;
    use std::thread;
    use tempfile::NamedTempFile;

    use crate::filewrapper::{FileWrapper, SendFile};
    use crate::globals::WSGIGlobals;
    use crate::pyutils::with_gil;
    use crate::request::{ParsingStage, WSGIRequest};
    use crate::response::{handle_request, WSGIResponse, HTTP400, HTTP500};
    use crate::startresponse::{StartResponse, WriteResponse};
    use crate::transport::SetBlocking;

    fn make_globals(py: Python) -> (WSGIGlobals, SocketAddr) {
        let server_name = "127.0.0.1";
        let port = "0";
        let sn = "/foo";
        (
            WSGIGlobals::new(server_name, port, sn, py),
            (server_name.to_string() + ":" + port).parse().unwrap(),
        )
    }

    #[test]
    fn test_create() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"li = iter([b"Hello", b"world", b"!"])"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let pylist = locals.get_item(py, "li").unwrap().as_object().clone_ref(py);
                let environ = PyDict::new(py);
                let headers = vec![(
                    "200 OK".to_string(),
                    vec![("Content-type".to_string(), "text/plain".to_string())],
                )];
                let sr = StartResponse::new(environ, headers, py).unwrap();
                let mut resp = WSGIResponse::new();
                resp.set_pyobject(pylist, py);
                assert!(resp.iterable.is_some());
                resp.start_response = Some(sr.as_object().clone_ref(py));
                let mut expectedv: Vec<&[u8]> = Vec::new();
                expectedv.push(
                    b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nVia: pyruvate\r\n\r\nHello",
                );
                expectedv.push(b"world");
                expectedv.push(b"!");
                for expected in expectedv {
                    match resp.render_next_chunk(py) {
                        Err(e) => {
                            debug!("Error encountered: {:?}", e);
                            assert!(false);
                        }
                        Ok(()) => {
                            assert!(!resp.last_chunk_or_file_sent);
                            debug!("current chunk: {:?}", resp.current_chunk);
                            assert!(resp
                                .current_chunk
                                .iter()
                                .zip(expected.iter())
                                .all(|(p, q)| p == q));
                            resp.current_chunk.clear();
                        }
                    }
                }
                match resp.render_next_chunk(py) {
                    Ok(()) => {
                        assert!(resp.last_chunk_or_file_sent);
                    }
                    Err(_) => assert!(false),
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_iterator() {
        // From the PEP:
        // When called by the server, the application object must return an iterable yielding zero or more bytestrings.
        // This can be accomplished in a variety of ways, such as by returning a list of bytestrings,
        // or by the application being a generator function that yields bytestrings,
        // or by the application being a class whose instances are iterable.
        // Regardless of how it is accomplished,
        // the application object must always return an iterable yielding zero or more bytestrings.
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"it = iter([b'Hello', b' world', b'!'])"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let pyit = locals.get_item(py, "it").unwrap().as_object().clone_ref(py);
                let environ = PyDict::new(py);
                let headers = vec![(
                    "200 OK".to_string(),
                    vec![("Content-type".to_string(), "text/plain".to_string())],
                )];
                let sr = StartResponse::new(environ, headers, py).unwrap();
                let mut resp = WSGIResponse::new();
                resp.set_pyobject(pyit, py);
                resp.start_response = Some(sr.as_object().clone_ref(py));
                let mut expected: Vec<&[u8]> = Vec::new();
                expected.push(
                    b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nVia: pyruvate\r\n\r\nHello",
                );
                expected.push(b" world");
                expected.push(b"!");
                for word in expected {
                    match resp.render_next_chunk(py) {
                        Err(e) => {
                            debug!("Error encountered: {:?}", e);
                            assert!(false);
                        }
                        Ok(()) => {
                            assert!(!resp.last_chunk_or_file_sent);
                            debug!("Bytes: {:?}", &resp.current_chunk[..]);
                            assert!(resp.current_chunk == word);
                            resp.current_chunk.clear();
                        }
                    }
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        };
        // 'iterable' is a list of bytestrings:
        match py.run(r#"it = [b'Hello', b'world', b'!']"#, None, Some(&locals)) {
            Ok(_) => {
                let pyit = locals.get_item(py, "it").unwrap().as_object().clone_ref(py);
                let environ = PyDict::new(py);
                let headers = vec![(
                    "200 OK".to_string(),
                    vec![("Content-type".to_string(), "text/plain".to_string())],
                )];
                let sr = StartResponse::new(environ, headers, py).unwrap();
                let mut resp = WSGIResponse::new();
                resp.set_pyobject(pyit, py);
                resp.start_response = Some(sr.as_object().clone_ref(py));
                let mut expected: Vec<&[u8]> = Vec::new();
                expected.push(
                    b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nVia: pyruvate\r\n\r\nHello",
                );
                expected.push(b"world");
                expected.push(b"!");
                for word in expected {
                    match resp.render_next_chunk(py) {
                        Ok(()) => {
                            debug!("{:?}", &resp.current_chunk[..]);
                            assert!(resp.current_chunk == word);
                            resp.current_chunk.clear();
                        }
                        Err(_) => assert!(false),
                    }
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_set_pyobject() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(r#"li = [b"Hello", b"world", b"!"]"#, None, Some(&locals)) {
            Ok(_) => {
                let pylist = locals.get_item(py, "li").unwrap().as_object().clone_ref(py);
                let mut resp = WSGIResponse::new();
                let refcnt = pylist.get_refcnt(py);
                resp.set_pyobject(pylist, py);
                match &resp.pyobject {
                    Some(po) => assert!(po.get_refcnt(py) == refcnt + 1),
                    None => assert!(false),
                }
            }
            _ => assert!(false),
        }
    }

    #[test]
    fn test_set_error() {
        let mut resp = WSGIResponse::new();
        resp.set_error_500();
        assert_eq!(&resp.current_chunk[..], HTTP500);
        assert!(resp.last_chunk_or_file_sent);
    }

    #[test]
    fn test_set_bad_request() {
        let mut resp = WSGIResponse::new();
        resp.set_bad_request_400();
        assert_eq!(&resp.current_chunk[..], HTTP400);
        assert!(resp.last_chunk_or_file_sent);
    }

    #[test]
    fn test_write_chunk() {
        let mut r = WSGIResponse::new();
        r.current_chunk = b"Foo 42".to_vec();
        r.last_chunk_or_file_sent = true;
        let addr: SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 6];
            conn.read(&mut buf).unwrap();
            snd.clone().send(buf).unwrap();
            rx.recv().unwrap();
            drop(conn);
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect to server");
        connection.set_blocking().unwrap();
        debug!("Response SendFileInfo: {:?}", r.sendfileinfo);
        with_gil(|py, gs| match r.write_chunk(&mut connection, py, gs) {
            Err(_) => {
                assert!(false);
            }
            Ok(true) => {
                let b = got.recv().unwrap();
                assert!(&b[..] == b"Foo 42");
            }
            _ => assert!(false),
        });
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_write_chunk_sendfile() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr: SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let mut tmp = NamedTempFile::new().unwrap();
        let mut f = tmp.reopen().unwrap();
        f.seek(std::io::SeekFrom::Start(0)).unwrap();
        let fw = FileWrapper::new(py, f.as_raw_fd(), 42).unwrap();
        let mut r = WSGIResponse::new();
        r.set_pyobject(fw.as_object().clone_ref(py), py);
        r.current_chunk = b"Foo 42".to_vec();
        r.last_chunk_or_file_sent = true;
        r.sendfileinfo = true;
        tmp.write_all(b"Hello World!\n").unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 19];
            conn.read(&mut buf).unwrap();
            conn.read(&mut buf[6..]).unwrap();
            snd.clone().send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        with_gil(|py, gs| match r.write_chunk(&mut connection, py, gs) {
            Err(_) => {
                assert!(false);
            }
            Ok(_) => {
                let b = got.recv().unwrap();
                assert_eq!(&b[..], b"Foo 42Hello World!\n");
            }
        });
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_write_chunk_sendfile_no_filewrapper() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr: SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let fw = py.None().as_object().clone_ref(py);
        let mut r = WSGIResponse::new();
        r.set_pyobject(fw, py);
        r.current_chunk = b"Foo 42".to_vec();
        r.last_chunk_or_file_sent = true;
        r.sendfileinfo = true;
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 10];
            conn.read(&mut buf).unwrap();
            snd.clone().send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        with_gil(|py, gs| match r.write_chunk(&mut connection, py, gs) {
            Err(_) => {
                assert!(false);
            }
            Ok(true) => {
                let b = got.recv().unwrap();
                assert_eq!(&b[..], b"Foo 42\0\0\0\0");
            }
            _ => assert!(false),
        });
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_handle_request() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    return [b"Hello world!\n"]

app = simple_app"#,
            None,
            Some(&locals),
        );
        match app {
            Ok(_) => {
                let (g, _) = make_globals(py);
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
                let mut req = WSGIRequest::new(16, String::new());
                req.append(raw);
                req.parse_data();
                handle_request(&app, &g, &mut req, py);
                if let Some(resp) = Arc::get_mut(&mut req.response).unwrap() {
                    resp.render_next_chunk(py).unwrap();
                    let expected = b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nExpires: Sat, 1 Jan 2000 00:00:00 GMT\r\nVia: pyruvate\r\n\r\nHello world!\n";
                    assert!(expected.len() == resp.current_chunk.len());
                    assert!(resp
                        .current_chunk
                        .iter()
                        .zip(expected.iter())
                        .all(|(p, q)| p == q));
                } else {
                    assert!(false);
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_handle_request_generator() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    yield b"Hello world!\n"

app = simple_app"#,
            None,
            Some(&locals),
        );
        match app {
            Ok(_) => {
                let (g, _) = make_globals(py);
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                let raw = b"GET /foo HTTP/1.1\r\n\r\n";
                let mut req = WSGIRequest::new(16, String::new());
                req.append(raw);
                req.parse_data();
                handle_request(&app, &g, &mut req, py);
                if let Some(resp) = Arc::get_mut(&mut req.response).unwrap() {
                    resp.render_next_chunk(py).unwrap();
                    let expected =
                        b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nVia: pyruvate\r\n\r\nHello world!\n";
                    assert!(expected.len() == resp.current_chunk.len());
                    assert!(resp
                        .current_chunk
                        .iter()
                        .zip(expected.iter())
                        .all(|(p, q)| p == q));
                } else {
                    assert!(false);
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_handle_request_multi_chunk() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT"), ('Content-Length', 13)]
    start_response(status, response_headers)
    return [b"Hello ", b"world!\n"]

app = simple_app"#, None, Some(&locals));
        match app {
            Ok(_) => {
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                let (g, _) = make_globals(py);
                let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
                let mut req = WSGIRequest::new(16, String::new());
                req.append(raw);
                req.parse_data();
                handle_request(&app, &g, &mut req, py);
                if let Some(resp) = Arc::get_mut(&mut req.response).unwrap() {
                    resp.render_next_chunk(py).unwrap();
                    let mut expected: Vec<&[u8]> = Vec::new();
                    expected.push(b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nExpires: Sat, 1 Jan 2000 00:00:00 GMT\r\nContent-Length: 13\r\nVia: pyruvate\r\n\r\nHello ");
                    expected.push(b"world!\n");
                    for word in expected {
                        debug!("{:?}", &resp.current_chunk[..]);
                        assert_eq!(resp.current_chunk, word);
                        resp.current_chunk.clear();
                        match resp.render_next_chunk(py) {
                            Ok(_) => {}
                            _ => assert!(false),
                        }
                    }
                    assert!(resp.last_chunk_or_file_sent);
                    assert!(resp
                        .start_response
                        .as_mut()
                        .unwrap()
                        .extract::<&StartResponse>(py)
                        .unwrap()
                        .content_complete(py));
                } else {
                    assert!(false);
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_handle_request_application_error() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    raise Exception("Baz")

app = simple_app"#,
            None,
            Some(&locals),
        );
        match app {
            Ok(_) => {
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                let (g, _) = make_globals(py);
                let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
                let mut req = WSGIRequest::new(16, String::new());
                req.append(raw);
                req.parse_data();
                handle_request(&app, &g, &mut req, py);
                if let Some(resp) = Arc::get_mut(&mut req.response).unwrap() {
                    if let Err(e) = resp.render_next_chunk(py) {
                        e.print_and_set_sys_last_vars(py);
                        assert!(false);
                    }
                    let expected = b"HTTP/1.1 500 Internal Server Error\r\n\r\n";
                    debug!("{:?}", &resp.current_chunk[..]);
                    assert!(resp
                        .current_chunk
                        .iter()
                        .zip(expected.iter())
                        .all(|(p, q)| p == q));
                    assert!(resp.last_chunk_or_file_sent);
                } else {
                    assert!(false);
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_handle_request_result_not_iterable() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    return None

app = simple_app"#,
            None,
            Some(&locals),
        );
        match app {
            Ok(_) => {
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                let (g, _) = make_globals(py);
                let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
                let mut req = WSGIRequest::new(16, String::new());
                req.append(raw);
                req.parse_data();
                handle_request(&app, &g, &mut req, py);
                if let Some(resp) = Arc::get_mut(&mut req.response).unwrap() {
                    resp.render_next_chunk(py).unwrap();
                    let expected = b"HTTP/1.1 500 Internal Server Error\r\n\r\n";
                    debug!("{:?}", &resp.current_chunk[..]);
                    assert!(resp
                        .current_chunk
                        .iter()
                        .zip(expected.iter())
                        .all(|(p, q)| p == q));
                    assert!(resp.last_chunk_or_file_sent);
                } else {
                    assert!(false);
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_handle_request_bad_request() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    return None

app = simple_app"#,
            None,
            Some(&locals),
        );
        match app {
            Ok(_) => {
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                let (g, _) = make_globals(py);
                let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
                let mut req = WSGIRequest::new(16, String::new());
                req.append(raw);
                req.parse_data();
                let mut req = WSGIRequest::new(16, String::new());
                req.stage = ParsingStage::HeadersError;
                assert!(req.is_bad_request());
                handle_request(&app, &g, &mut req, py);
                if let Some(resp) = Arc::get_mut(&mut req.response).unwrap() {
                    let expected = b"HTTP/1.1 400 Bad Request\r\n\r\n";
                    debug!("{:?}", &resp.current_chunk[..]);
                    assert!(expected
                        .iter()
                        .zip(resp.current_chunk.iter())
                        .all(|(p, q)| p == q));
                    assert!(resp.last_chunk_or_file_sent);
                } else {
                    assert!(false);
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_render_next_chunk_no_iterator() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![("Content-type".to_string(), "text/plain".to_string())],
        )];
        let sr = StartResponse::new(environ, headers, py).unwrap();
        let mut resp = WSGIResponse::new();
        resp.start_response = Some(sr.as_object().clone_ref(py));
        resp.iterable = Some(py.None());
        match resp.render_next_chunk(py) {
            Err(e) => {
                assert!(py.get_type::<TypeError>() == e.get_type(py));
            }
            _ => assert!(false),
        }
    }

    #[test]
    fn test_render_next_chunk_no_bytes_in_iterator() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(r#"li = ["Hello", 42, None]"#, None, Some(&locals)) {
            Ok(_) => {
                let pylist = locals.get_item(py, "li").unwrap().as_object().clone_ref(py);
                let environ = PyDict::new(py);
                let headers = vec![(
                    "200 OK".to_string(),
                    vec![("Content-type".to_string(), "text/plain".to_string())],
                )];
                let sr = StartResponse::new(environ, headers, py).unwrap();
                let mut resp = WSGIResponse::new();
                resp.start_response = Some(sr.as_object().clone_ref(py));
                resp.set_pyobject(pylist, py);
                match resp.render_next_chunk(py) {
                    Ok(()) => {
                        assert!(resp.last_chunk_or_file_sent);
                    }
                    Err(_) => assert!(false),
                }
            }
            _ => assert!(false),
        }
    }
}
