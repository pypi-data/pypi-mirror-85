#![allow(clippy::transmute_ptr_to_ptr, clippy::zero_ptr)] // suppress warnings in py_class invocation
use cpython::{PyClone, PyDict, PyList, PyObject, PyResult, PyTuple, Python};
use log::error;
use std::cell::{Cell, RefCell};
use std::cmp;

use crate::request::CONTENT_LENGTH_HEADER;

type WSGIHeaders = Vec<(String, Vec<(String, String)>)>;

py_class!(pub class StartResponse |py| {

    data environ: PyDict;
    data headers_set: RefCell<WSGIHeaders>;
    data headers_sent: RefCell<WSGIHeaders>;
    data content_length: Cell<Option<usize>>;
    data content_bytes_written: Cell<usize>;

    def __new__(_cls, environ: PyDict)-> PyResult<StartResponse> {
        StartResponse::create_instance(py, environ, RefCell::new(Vec::new()), RefCell::new(Vec::new()), Cell::new(None), Cell::new(0))
    }

    def __call__(&self, status: PyObject, headers: PyObject, exc_info: Option<PyObject> = None) -> PyResult<PyObject> {
        let response_headers : &PyList = headers.extract(py)?;
        if !exc_info.is_none() {
            error!("exc_info from application: {:?}", exc_info);
        }
        let mut rh = Vec::<(String, String)>::new();
        for ob in response_headers.iter(py) {
            let tp = ob.extract::<PyTuple>(py)?;
            rh.push((tp.get_item(py, 0).to_string(), tp.get_item(py, 1).to_string()));
        }
        self.headers_set(py).replace(vec![(status.to_string(), rh)]);
        Ok(py.None())
    }

});

pub trait WriteResponse {
    // Put this in a trait for more flexibility.
    // PyO3 can't handle some types we are using here.
    fn new(
        environ: PyDict,
        headers_set: Vec<(String, Vec<(String, String)>)>,
        py: Python,
    ) -> PyResult<StartResponse>;
    fn content_complete(&self, py: Python) -> bool;
    fn write(&mut self, data: &[u8], output: &mut Vec<u8>, py: Python);
    fn environ(&self, py: Python) -> PyDict;
    fn content_length(&self, py: Python) -> Option<usize>;
}

impl WriteResponse for StartResponse {
    fn new(environ: PyDict, headers_set: WSGIHeaders, py: Python) -> PyResult<StartResponse> {
        StartResponse::create_instance(
            py,
            environ,
            RefCell::new(headers_set),
            RefCell::new(Vec::new()),
            Cell::new(None),
            Cell::new(0),
        )
    }

    fn content_complete(&self, py: Python) -> bool {
        if let Some(length) = self.content_length(py).get() {
            self.content_bytes_written(py).get() >= length
        } else {
            false
        }
    }

    fn write(&mut self, data: &[u8], output: &mut Vec<u8>, py: Python) {
        if self.headers_sent(py).borrow().is_empty() {
            if self.headers_set(py).borrow().is_empty() {
                panic!("write() before start_response()")
            }
            // Before the first output, send the stored headers
            self.headers_sent(py)
                .replace(self.headers_set(py).borrow().clone());
            let respinfo = self.headers_set(py).borrow_mut().pop(); // headers_sent|set should have only one element
            match respinfo {
                Some(respinfo) => {
                    let response_headers: Vec<(String, String)> = respinfo.1;
                    let status: String = respinfo.0;
                    output.extend(b"HTTP/1.1 ");
                    output.extend(status.as_bytes());
                    output.extend(b"\r\n");
                    for header in response_headers.iter() {
                        let headername = &header.0;
                        output.extend(headername.as_bytes());
                        output.extend(b": ");
                        output.extend(header.1.as_bytes());
                        output.extend(b"\r\n");
                        if headername.to_ascii_uppercase() == CONTENT_LENGTH_HEADER {
                            match header.1.parse::<usize>() {
                                Ok(length) => {
                                    self.content_length(py).set(Some(length));
                                }
                                Err(e) => error!("Could not parse Content-Length header: {:?}", e),
                            }
                        }
                    }
                    output.extend(b"Via: pyruvate\r\n")
                }
                None => {
                    error!("write(): No respinfo!");
                }
            }
            output.extend(b"\r\n");
        }
        match self.content_length(py).get() {
            Some(length) => {
                let cbw = self.content_bytes_written(py).get();
                if length > cbw {
                    let num = cmp::min(length - cbw, data.len());
                    output.extend(&data[..num]);
                    self.content_bytes_written(py).set(cbw + num);
                }
            }
            None => output.extend(data),
        };
    }

    fn environ(&self, py: Python) -> PyDict {
        self.environ(py).clone_ref(py)
    }

    fn content_length(&self, py: Python) -> Option<usize> {
        self.content_length(py).get()
    }
}

#[cfg(test)]
mod tests {
    use cpython::{PyClone, PyDict, Python};
    use log::LevelFilter;
    use simplelog::{Config, WriteLogger};
    use std::env::temp_dir;
    use std::fs::File;
    use std::io::Read;

    use crate::startresponse::{StartResponse, WriteResponse};

    #[test]
    fn test_write() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![("Content-type".to_string(), "text/plain".to_string())],
        )];
        let mut sr = StartResponse::new(environ, headers, py).unwrap();
        let mut output: Vec<u8> = Vec::new();
        let data = b"Hello world!\n";
        assert!(!sr.content_complete(py));
        sr.write(data, &mut output, py);
        let expected =
            b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nVia: pyruvate\r\n\r\nHello world!\n";
        assert!(output.iter().zip(expected.iter()).all(|(p, q)| p == q));
        assert!(!sr.content_complete(py));
    }

    #[test]
    fn test_honour_content_length_header() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let environ = PyDict::new(py);
        let headers = vec![(
            "200 OK".to_string(),
            vec![
                ("Content-type".to_string(), "text/plain".to_string()),
                ("Content-length".to_string(), "5".to_string()),
            ],
        )];
        let mut sr = StartResponse::new(environ, headers, py).unwrap();
        let mut output: Vec<u8> = Vec::new();
        let data = b"Hello world!\n";
        assert!(!sr.content_complete(py));
        sr.write(data, &mut output, py);
        let expected =
            b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-length: 5\r\nVia: pyruvate\r\n\r\nHello";
        assert_eq!(sr.content_length(py).get(), Some(5));
        assert_eq!(sr.content_bytes_written(py).get(), 5);
        assert!(sr.content_complete(py));
        assert!(expected.iter().zip(output.iter()).all(|(p, q)| p == q));
    }

    #[test]
    fn test_exc_info_is_none() {
        // do not display an error message when exc_info passed
        // by application is None
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        let pycode = py.run(
            r#"
status = '200 OK'
response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
exc_info = 'Foo'
"#,
            None,
            Some(&locals),
        );
        match pycode {
            Ok(_) => {
                let status = locals.get_item(py, "status").unwrap();
                let headers = locals.get_item(py, "response_headers").unwrap();
                let exc_info = locals.get_item(py, "exc_info").unwrap();
                let environ = PyDict::new(py);
                // create logger
                let mut path = temp_dir();
                path.push("foo42.log");
                let path = path.into_os_string();
                WriteLogger::init(
                    LevelFilter::Info,
                    Config::default(),
                    File::create(&path).unwrap(),
                )
                .unwrap();

                let sr = StartResponse::new(environ, Vec::new(), py).unwrap();
                match sr.__call__(py, status.clone_ref(py), headers.clone_ref(py), None) {
                    Ok(pynone) if pynone == py.None() => {
                        let mut errs = File::open(&path).unwrap();
                        let mut got = String::new();
                        errs.read_to_string(&mut got).unwrap();
                        assert_eq!(got.len(), 0);
                    }
                    _ => assert!(false),
                }
                match sr.__call__(py, status, headers, Some(exc_info)) {
                    Ok(pynone) if pynone == py.None() => {
                        let mut errs = File::open(&path).unwrap();
                        let mut got = String::new();
                        errs.read_to_string(&mut got).unwrap();
                        assert!(got.len() > 0);
                        assert!(got.contains("Foo"));
                    }
                    _ => assert!(false),
                }
            }
            _ => assert!(false),
        }
    }
}
