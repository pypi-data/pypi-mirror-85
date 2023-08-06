use cpython::{PyObject, Python};
use log::{debug, error, info};
use mio::{Events, Interest, Poll, Token};
use python3_sys::{PyEval_RestoreThread, PyEval_SaveThread};
use std::collections::HashMap;
use std::io;
use std::time::Duration;

use crate::globals::WSGIGlobals;
use crate::request::WSGIRequest;
use crate::transport::{would_block, Listener, Read, Result};
use crate::workerpool::WorkerPool;
use crate::workers::{write_blocking_worker, write_non_blocking_worker};

pub const SERVER: Token = Token(0);
const READBUFSIZE: usize = 16384;
const POLL_TIMEOUT: u64 = 100;

fn next(current: &mut Token) -> Token {
    let next = current.0;
    current.0 += 1;
    Token(next)
}

pub struct Server<L: Listener> {
    poll: Poll,
    events: Events,
    listener: L,
    workers: WorkerPool<L::Connected>,
    connections: HashMap<Token, L::Connected>,
    requests: HashMap<Token, WSGIRequest>,
    current_token: Token,
    max_number_headers: usize,
}

impl<'g, L: 'static + Listener> Server<L> {
    pub fn new(
        application: PyObject,
        globals: &WSGIGlobals<'g>,
        listener: L,
        num_workers: usize,
        write_blocking: bool,
        max_number_headers: usize,
        py: Python,
    ) -> io::Result<Server<L>> {
        let workers = WorkerPool::new(
            String::from(globals.server_name),
            String::from(globals.server_port),
            globals.script_name.to_string(),
            application,
            if write_blocking {
                write_blocking_worker::<L, L::Connected>
            } else {
                write_non_blocking_worker::<L, L::Connected>
            },
            num_workers,
            py,
        );
        let mut listener = listener;
        let poll = Poll::new()?;
        poll.registry()
            .register(&mut listener, SERVER, Interest::READABLE)?;

        Ok(Server {
            poll,
            events: Events::with_capacity(1024),
            listener,
            workers,
            connections: HashMap::new(),
            requests: HashMap::new(),
            current_token: Token(SERVER.0 + 1),
            max_number_headers,
        })
    }

    /// Returns a new WSGIRequest if reading is successful.
    fn handle_read_event(
        &self,
        connection: &mut impl Read,
        request: Option<WSGIRequest>,
    ) -> io::Result<WSGIRequest> {
        let mut connection_closed = false;
        let mut req = match request {
            Some(request) => request,
            None => {
                debug!("creating new WSGI request");
                WSGIRequest::new(self.max_number_headers, connection.peer_addr())
            }
        };
        // We can (maybe) read from the connection.
        loop {
            let mut buf = [0; READBUFSIZE];
            match connection.read(&mut buf) {
                Ok(0) => {
                    // Reading 0 bytes means the other side has closed the
                    // connection or is done writing, then so are we.
                    debug!("Reading 0 bytes, consider reading done");
                    // req.parse_data();
                    connection_closed = true;
                    break;
                }
                Ok(n) => {
                    debug!("appending {} bytes to buffer", n);
                    req.append(&buf[..n])
                }
                // Would block "errors" are the OS's way of saying that the
                // connection is not actually ready to perform this I/O operation.
                Err(ref err) if would_block(err) => {
                    debug!("handle_read_event would block");
                    break;
                }
                // Other errors we'll consider fatal.
                Err(err) => return Err(err),
            }
        }

        if connection_closed & !req.stage.complete() {
            debug!("Connection closed");
            Err(io::Error::new(io::ErrorKind::Other, "Incomplete request"))
        } else {
            Ok(req)
        }
    }

    pub fn poll_once(&mut self) -> Result<()> {
        match self
            .poll
            .poll(&mut self.events, Some(Duration::from_millis(POLL_TIMEOUT)))
        {
            Ok(_) => {
                for event in self.events.iter() {
                    match event.token() {
                        SERVER => {
                            while let Ok(mut connection) = self.listener.accept() {
                                let token = next(&mut self.current_token);
                                debug!("current token: {:?}", token);

                                self.poll.registry().register(
                                    &mut connection,
                                    token,
                                    Interest::READABLE,
                                )?;
                                self.connections.insert(token, connection);
                            }
                        }
                        token if event.is_readable() => {
                            // (maybe) received an event for a connection.
                            if let Some(mut connection) = self.connections.remove(&token) {
                                let req = self.requests.remove(&token);
                                match self.handle_read_event(&mut connection, req) {
                                    Ok(mut req) => {
                                        if req.parse_data() {
                                            debug!("Request complete, relaying to worker pool");
                                            self.workers.execute(token, req, Some(connection))?;
                                        } else {
                                            self.requests.insert(token, req);
                                            self.connections.insert(token, connection);
                                        }
                                    }
                                    Err(e) => {
                                        error!("Could not handle read event: {:?}", e);
                                    }
                                }
                            }
                        }
                        _ => (),
                    }
                }
            }
            Err(e) => return Err(Box::new(e)),
        }
        Ok(())
    }

    pub fn serve(&mut self) -> Result<()> {
        let py_thread_state = unsafe { PyEval_SaveThread() };
        info!(
            "pyruvate listening on {}",
            self.listener.local_addr_string()
        );
        loop {
            if let Err(e) = self.poll_once() {
                error!("Error processing poll events: {:?}", e);
                self.workers.join()?;
                break;
            }
        }
        unsafe { PyEval_RestoreThread(py_thread_state) };
        Ok(())
    }
}

#[cfg(test)]
mod tests {

    use cpython::{PyClone, PyDict, Python, PythonObject};
    use mio::net::TcpListener;
    use mio::Token;
    use std::io::{self, Write};
    use std::net::{SocketAddr, TcpStream};
    use std::ops::Range;
    use std::thread;
    use std::time::Duration;

    use crate::globals::WSGIGlobals;
    use crate::server::{next, Server};
    use crate::transport::Read;

    struct StreamMock {
        pub data: Vec<u8>,
        block_pos: usize,
        raise: bool,
        pos: usize,
        error: Option<io::ErrorKind>,
    }

    impl StreamMock {
        pub fn new(data: Vec<u8>, block_before_complete: bool, raise: bool) -> StreamMock {
            let block_pos = if block_before_complete {
                10
            } else {
                data.len()
            };
            StreamMock {
                data,
                block_pos,
                raise,
                pos: 0,
                error: None,
            }
        }

        pub fn read_slice(&mut self, range: Range<usize>, buf: &mut [u8]) -> usize {
            self.pos = range.start;
            let start = range.start;
            let num_bytes = range.end - self.pos;
            for idx in range {
                let offset = idx - start;
                match self.data.get(idx) {
                    Some(d) => {
                        buf[offset] = *d;
                        self.pos = self.pos + 1;
                    }
                    None => return offset,
                }
            }
            num_bytes
        }
    }

    impl io::Read for StreamMock {
        fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
            match self.error {
                None => {
                    let num_bytes = self.read_slice(0..self.block_pos, buf);
                    self.error = Some(io::ErrorKind::WouldBlock);
                    Ok(num_bytes)
                }
                Some(errkind) if errkind == io::ErrorKind::WouldBlock => {
                    self.error = Some(io::ErrorKind::Other);
                    Err(io::Error::new(
                        io::ErrorKind::WouldBlock,
                        "StreamMock blocking",
                    ))
                }
                Some(errkind) if errkind == io::ErrorKind::Other => {
                    self.error = Some(io::ErrorKind::WriteZero);
                    Ok(self.read_slice(self.block_pos..buf.len(), buf))
                }
                Some(_) => {
                    if self.raise {
                        Err(io::Error::new(
                            io::ErrorKind::BrokenPipe,
                            "StreamMock raising",
                        ))
                    } else {
                        Ok(0)
                    }
                }
            }
        }
    }

    impl Read for StreamMock {
        fn peer_addr(&self) -> String {
            String::from("foo42")
        }
    }

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
    fn test_next() {
        let mut start = Token(0);
        for idx in 0..6 {
            let got = next(&mut start);
            assert_eq!(Token(idx), got);
            assert_eq!(start.0, idx + 1);
        }
    }

    #[test]
    fn test_handle_read_event() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let (g, si) = make_globals(py);
        let listener = TcpListener::bind(si).unwrap();
        let server = Server::new(py.None(), &g, listener, 2, false, 16, py).unwrap();
        let expected = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
        let mut s = StreamMock::new(expected.to_vec(), true, false);
        // read interrupted by WouldBlock, block will occur
        // before complete parsing of request is possible
        match server.handle_read_event(&mut s, None) {
            Ok(mut req) => {
                assert!(req.data.len() == 10);
                assert!(expected.iter().zip(req.data.iter()).all(|(p, q)| p == q));
                let res = req.parse_data();
                assert!(req.data.len() == 10);
                assert!(!res);
            }
            Err(_) => {
                assert!(false);
            }
        }
        let mut s = StreamMock::new(expected.to_vec(), false, false);
        // read interrupted by WouldBlock, block will occur
        // when complete parsing of request is possible
        match server.handle_read_event(&mut s, None) {
            Ok(mut req) => {
                assert!(req.data.iter().zip(expected.iter()).all(|(p, q)| p == q));
                assert!(req.parse_data());
            }
            Err(_) => {
                assert!(false);
            }
        }
        let mut s = StreamMock::new(expected.to_vec(), true, true);
        // read until WouldBlock, block will occur
        // before complete parsing of request is possible
        // and then raise BrokenPipe
        match server.handle_read_event(&mut s, None) {
            Ok(req) => match server.handle_read_event(&mut s, Some(req)) {
                Ok(_) => assert!(false),
                Err(e) => {
                    assert!(e.kind() == io::ErrorKind::BrokenPipe);
                }
            },
            Err(_) => assert!(false),
        }
    }

    #[test]
    fn test_handle_read_event_too_many_headers() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let (g, si) = make_globals(py);
        let listener = TcpListener::bind(si).unwrap();
        let server = Server::new(py.None(), &g, listener, 2, false, 16, py).unwrap();
        let expected = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\nH1: 1\r\nH2: 2\r\nH3: 3\r\nH4: 4\r\nH5: 5\r\nH6: 6\r\nH7: 7\r\nH8: 8\r\nH9: 9\r\nH10: 10\r\nH11: 11\r\nH12: 12\r\n\r\n";
        let mut s = StreamMock::new(expected.to_vec(), true, false);
        // read interrupted by WouldBlock, block will occur
        // before complete parsing of request is possible
        match server.handle_read_event(&mut s, None) {
            Ok(req) => match server.handle_read_event(&mut s, Some(req)) {
                Ok(_) => assert!(false),
                Err(e) => {
                    assert!(e.kind() == io::ErrorKind::Other);
                }
            },
            Err(_) => assert!(false),
        }
    }

    #[test]
    fn test_create_blocking_server() {
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
                let (g, si) = make_globals(py);
                let listener = TcpListener::bind(si).unwrap();
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                match Server::new(app, &g, listener, 2, true, 16, py) {
                    Ok(got) => {
                        assert!(got.current_token == Token(1));
                    }
                    Err(_) => {
                        assert!(false);
                    }
                }
            }
            _ => assert!(false),
        }
    }

    #[test]
    fn test_create_non_blocking_server() {
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
                let (g, si) = make_globals(py);
                let listener = TcpListener::bind(si).unwrap();
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                match Server::new(app, &g, listener, 2, false, 16, py) {
                    Ok(got) => {
                        assert!(got.current_token == Token(1));
                    }
                    Err(_) => {
                        assert!(false);
                    }
                }
            }
            _ => assert!(false),
        }
    }

    #[test]
    fn test_create_non_blocking_server_socket_activation() {
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
                let (g, si) = make_globals(py);
                let listener = TcpListener::bind(si).unwrap();
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                match Server::new(app, &g, listener, 2, false, 16, py) {
                    Ok(got) => {
                        assert!(got.current_token == Token(1));
                    }
                    Err(_) => {
                        assert!(false);
                    }
                }
            }
            _ => assert!(false),
        }
    }

    #[test]
    fn test_server_poll_once() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ]
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
                let si: SocketAddr = "127.0.0.1:7878".parse().unwrap();
                let listener = TcpListener::bind(si).unwrap();
                match Server::new(app, &g, listener, 1, true, 16, py) {
                    Ok(mut got) => {
                        // accept
                        got.poll_once().unwrap();
                        // create request in separate thread
                        let t = thread::spawn(move || {
                            let mut connection =
                                TcpStream::connect_timeout(&si, Duration::from_millis(1000))
                                    .expect("Failed to connect to server");
                            let req = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\n\r\n";
                            match connection.write(req) {
                                Ok(num_bytes) => assert_eq!(num_bytes, req.len()),
                                Err(_) => assert!(false),
                            };
                        });
                        // read + propagate HTTPrequest
                        if let Err(_) = got.poll_once() {
                            // accept connection
                            assert!(false);
                        }
                        if let Err(_) = got.poll_once() {
                            // handle request in worker
                            assert!(false);
                        }
                        t.join().unwrap();
                    }
                    Err(_) => {
                        assert!(false);
                    }
                }
            }
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }
}
