use cpython::{
    NoArgs, ObjectProtocol, PyBytes, PyClone, PyDict, PyResult, PyTuple, Python, PythonObject,
    ToPyObject,
};
use httparse::{self};
use log::{debug, error};
use std::sync::Arc;
use urlencoding::decode;

use crate::globals::WSGIGlobals;
use crate::response::WSGIResponse;

// https://tools.ietf.org/html/rfc7230#section-3.2
// Each header field consists of a case-insensitive field name ...
pub const CONTENT_LENGTH_HEADER: &str = "CONTENT-LENGTH";
const CONTENT_TYPE_HEADER: &str = "CONTENT-TYPE";
const CONTENT_TYPE: &str = "CONTENT_TYPE";
const REQUEST_METHOD: &str = "REQUEST_METHOD";
const PATH_INFO: &str = "PATH_INFO";
const QUERY_STRING: &str = "QUERY_STRING";
const SERVER_PROTOCOL: &str = "SERVER_PROTOCOL";

#[derive(PartialEq, Debug)]
pub enum ParsingStage {
    NotParsed,
    HeadersSuccess,
    HeadersError, // parsing headers returned an error, covering the too many headers case
    ContentPartial,
    ContentComplete,
}

impl ParsingStage {
    pub fn headers_complete(&self) -> bool {
        (self != &ParsingStage::NotParsed) && (self != &ParsingStage::HeadersError)
    }

    pub fn complete(&self) -> bool {
        (self == &ParsingStage::ContentComplete) | (self == &ParsingStage::HeadersError)
    }
}

pub struct WSGIRequest {
    pub data: Vec<u8>,
    pub stage: ParsingStage,
    pub content_length: usize,
    pub content_start: usize,
    pub http_headers: Vec<(String, String)>,
    pub peer_addr: String,
    pub response: Arc<Option<WSGIResponse>>,
    num_headers: usize,
}

impl WSGIRequest {
    pub fn new(num_headers: usize, peer_addr: String) -> WSGIRequest {
        WSGIRequest {
            data: Vec::new(),
            stage: ParsingStage::NotParsed,
            content_length: 0,
            content_start: 0,
            http_headers: Vec::new(),
            peer_addr,
            response: Arc::new(None),
            num_headers,
        }
    }

    #[inline]
    pub fn append(&mut self, data: &[u8]) {
        self.data.extend_from_slice(data);
    }

    fn parse_headers(&mut self) -> ParsingStage {
        let mut headers = vec![httparse::EMPTY_HEADER; self.num_headers];
        let mut req = httparse::Request::new(&mut headers);
        let length = self.data.len();
        match req.parse(&self.data) {
            Ok(res) => {
                if let httparse::Status::Complete(size) = res {
                    self.content_start = size;
                    self.content_length = length - self.content_start;
                    for header in req.headers.iter() {
                        let uname = header.name.to_ascii_uppercase();
                        match uname.as_str() {
                            CONTENT_LENGTH_HEADER => {
                                if let Ok(val) = std::str::from_utf8(header.value) {
                                    if let Ok(parsedval) = val.parse() {
                                        self.content_length = parsedval;
                                    }
                                }
                            }
                            &_ => {
                                let key = if uname.as_str() == CONTENT_TYPE_HEADER {
                                    CONTENT_TYPE.to_string()
                                } else {
                                    let mut key = "HTTP_".to_string();
                                    key.push_str(&uname.replace("-", "_"));
                                    key
                                };
                                match std::str::from_utf8(header.value) {
                                    Ok(val) => self.http_headers.push((key, val.to_string())),
                                    Err(e) => {
                                        error!("{:?} encountered for value: {:?}", e, header.value);
                                        return ParsingStage::HeadersError;
                                    }
                                }
                            }
                        }
                    }
                    if let Some(method) = req.method {
                        self.http_headers
                            .push((REQUEST_METHOD.to_string(), method.to_string()));
                    }
                    if let Some(path) = req.path {
                        match decode(path) {
                            Ok(decoded) => {
                                let parts: Vec<&str> = decoded.splitn(2, '?').collect();
                                self.http_headers
                                    .push((PATH_INFO.to_string(), parts[0].to_string()));
                                if parts.len() > 1 {
                                    self.http_headers
                                        .push((QUERY_STRING.to_string(), parts[1].to_string()));
                                } else {
                                    self.http_headers
                                        .push((QUERY_STRING.to_string(), "".to_string()));
                                }
                            }
                            Err(e) => {
                                error!("Could not urldecode path info: {:?}", e);
                                return ParsingStage::HeadersError;
                            }
                        }
                    }
                    if let Some(version) = req.version {
                        if version > 1 {
                            error!("Unsupported version: {:?}", version);
                            return ParsingStage::HeadersError;
                        } else {
                            let protocol = format!("HTTP/1.{}", version);
                            self.http_headers
                                .push((SERVER_PROTOCOL.to_string(), protocol));
                        }
                    }
                    ParsingStage::HeadersSuccess
                } else {
                    ParsingStage::NotParsed
                }
            }
            Err(e) => {
                error!("Could not parse request: {:?}", e);
                ParsingStage::HeadersError
            }
        }
    }

    pub fn parse_data(&mut self) -> bool {
        if !self.stage.headers_complete() {
            debug!("Parsing request headers: {:?}", self.stage);
            self.stage = self.parse_headers();
        }
        if self.stage.headers_complete() {
            let length = self.data.len();
            self.stage = if self.content_length > length - self.content_start {
                // expecting more data, maybe from the next read
                debug!(
                    "Expecting more data; content_length: {}, length: {}, content_start: {}",
                    self.content_length, length, self.content_start
                );
                ParsingStage::ContentPartial
            } else {
                ParsingStage::ContentComplete
            }
        }
        self.stage.complete()
    }

    pub fn wsgi_environ(&self, globals: &WSGIGlobals, py: Python) -> PyResult<PyDict> {
        let io = &globals.io_module;
        let environ = globals.wsgi_environ.copy(py)?;
        for (k, v) in self.http_headers.iter() {
            environ.set_item(py, k, v)?;
        }
        environ.set_item(py, globals.peer_addr_key.clone_ref(py), &self.peer_addr)?;
        let input = io.call(py, "BytesIO", NoArgs, None)?;
        if self.content_length > 0 {
            environ.set_item(
                py,
                globals.content_length_key.clone_ref(py),
                self.content_length,
            )?;
            input.call_method(
                py,
                "write",
                PyTuple::new(
                    py,
                    &[PyBytes::new(
                        py,
                        &self.data[self.content_start..self.content_start + self.content_length],
                    )
                    .into_object()],
                ),
                None,
            )?;
            input.call_method(
                py,
                "seek",
                PyTuple::new(py, &[(0 as i32).to_py_object(py).into_object()]),
                None,
            )?;
        }
        environ.set_item(py, globals.wsgi_input_key.clone_ref(py), input)?;
        Ok(environ)
    }

    #[inline]
    pub fn get_response(&mut self) -> Option<&mut WSGIResponse> {
        if let Some(opt) = Arc::get_mut(&mut self.response) {
            if let Some(resp) = opt {
                return Some(resp);
            }
        }
        None
    }

    pub fn is_bad_request(&self) -> bool {
        self.stage == ParsingStage::HeadersError
    }
}

#[cfg(test)]
mod tests {
    use cpython::{NoArgs, ObjectProtocol, PyBytes, PyClone, PyString, Python, PythonObject};
    use log::debug;
    use std::net::SocketAddr;
    use std::sync::Arc;

    use crate::globals::WSGIGlobals;
    use crate::request::{ParsingStage, WSGIRequest};
    use crate::response::WSGIResponse;

    macro_rules! assert_header {
        ($got:ident, $py:ident, $key:literal, $value:expr) => {
            assert!(
                $got.get_item($py, $key)
                    .unwrap()
                    .extract::<PyString>($py)
                    .unwrap()
                    .to_string($py)
                    .unwrap()
                    == $value
            );
        };
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
    fn test_get() {
        let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nAuthorization: Basic YWRtaW46YWRtaW4=\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
        let mut got = WSGIRequest::new(16, String::new());
        got.append(raw);
        got.parse_data();
        assert!(got.http_headers.len() == 13);
        for (name, value) in got.http_headers.iter() {
            match name.as_str() {
                "HTTP_COOKIE" => assert!(&value[..] == "foo_language=en;"),
                "PATH_INFO" => assert!(&value[..] == "/foo42"),
                "QUERY_STRING" => assert!(&value[..] == "bar=baz"),
                "HTTP_ACCEPT" => assert!(&value[..] == "image/webp,*/*"),
                "HTTP_ACCEPT_LANGUAGE" => assert!(&value[..] == "de-DE,en-US;q=0.7,en;q=0.3"),
                "HTTP_ACCEPT_ENCODING" => assert!(&value[..] == "gzip, deflate"),
                "HTTP_AUTHORIZATION" => assert!(&value[..] == "Basic YWRtaW46YWRtaW4="),
                "HTTP_CONNECTION" => assert!(&value[..] == "keep-alive"),
                "REQUEST_METHOD" => assert!(&value[..] == "GET"),
                "HTTP_HOST" => assert!(&value[..] == "localhost:7878"),
                "HTTP_USER_AGENT" => {
                    let expected = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0";
                    assert_eq!(value, expected);
                }
                "HTTP_DNT" => assert_eq!(&value[..], "1"),
                "SERVER_PROTOCOL" => assert_eq!(&value[..], "HTTP/1.1"),
                &_ => {}
            }
        }
    }

    #[test]
    fn test_url_decode() {
        let raw = b"GET /foo%2042?bar=baz%20foo HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
        let mut got = WSGIRequest::new(16, String::new());
        got.append(raw);
        got.parse_data();
        assert!(got.http_headers.len() == 12);
        for (name, value) in got.http_headers.iter() {
            match name.as_str() {
                "HTTP_COOKIE" => assert!(&value[..] == "foo_language=en;"),
                "PATH_INFO" => assert!(&value[..] == "/foo 42"),
                "QUERY_STRING" => assert!(&value[..] == "bar=baz foo"),
                "HTTP_ACCEPT" => assert!(&value[..] == "image/webp,*/*"),
                "HTTP_ACCEPT_LANGUAGE" => assert!(&value[..] == "de-DE,en-US;q=0.7,en;q=0.3"),
                "HTTP_ACCEPT_ENCODING" => assert!(&value[..] == "gzip, deflate"),
                "HTTP_AUTHORIZATION" => assert!(&value[..] == "Basic YWRtaW46YWRtaW4="),
                "HTTP_CONNECTION" => assert!(&value[..] == "keep-alive"),
                "REQUEST_METHOD" => assert!(&value[..] == "GET"),
                "HTTP_HOST" => assert!(&value[..] == "localhost:7878"),
                "HTTP_USER_AGENT" => {
                    let expected = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0";
                    assert_eq!(value, expected);
                }
                "HTTP_DNT" => assert_eq!(&value[..], "1"),
                "SERVER_PROTOCOL" => assert_eq!(&value[..], "HTTP/1.1"),
                &_ => {}
            }
        }
    }

    #[test]
    fn test_error_url() {
        let raw = b"GET /foo 42?bar=baz foo HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
        let mut got = WSGIRequest::new(16, String::new());
        got.append(raw);
        match got.parse_data() {
            true => {
                assert!(got.stage == ParsingStage::HeadersError);
            }
            false => assert!(false),
        }
    }

    #[test]
    fn test_parse_body_once() {
        let raw = b"POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 27\r\n\r\nfield1=value1&field2=value2";
        let mut got = WSGIRequest::new(16, String::new());
        got.append(raw);
        got.parse_data();
        assert!(got.stage.complete());
        for (name, value) in got.http_headers.iter() {
            match name.as_str() {
                "CONTENT_TYPE" => {
                    let expected = "application/x-www-form-urlencoded";
                    assert_eq!(value, expected);
                }
                &_ => {}
            }
        }
        let body = &got.data[got.content_start..got.content_start + got.content_length];
        assert_eq!(body, b"field1=value1&field2=value2");
    }

    #[test]
    fn test_parse_multiple() {
        let raw1 = b"POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 41\r\n\r\nfield1=value1&field2=value2";
        let raw2 = b"&field3=value3";
        let mut got = WSGIRequest::new(16, String::new());
        got.append(raw1);
        got.parse_data();
        assert!(!got.stage.complete());
        assert!(got.content_length == 41);
        got.append(raw2);
        got.parse_data();
        assert!(got.stage.complete());
        assert!(got.content_length == 41);
        for (name, value) in got.http_headers.iter() {
            match name.as_str() {
                "CONTENT_TYPE" => {
                    let expected = "application/x-www-form-urlencoded";
                    assert_eq!(expected, value);
                }
                &_ => {}
            }
        }
        let expected = b"field1=value1&field2=value2&field3=value3";
        let body = &got.data[got.content_start..got.content_start + got.content_length];
        debug!("{:?}", body);
        assert!(body.iter().zip(expected.iter()).all(|(p, q)| p == q));
    }

    #[test]
    fn test_environ_dict() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let (g, _) = make_globals(py);
        let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nAuthorization: Basic YWRtaW46YWRtaW4=\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
        let mut req = WSGIRequest::new(16, String::from("192.168.1.23"));
        req.append(raw);
        req.parse_data();
        let got = req.wsgi_environ(&g, py).unwrap();
        assert_header!(got, py, "SERVER_NAME", "127.0.0.1");
        assert_header!(got, py, "SERVER_PORT", "0");
        assert_header!(got, py, "SCRIPT_NAME", "/foo");
        assert_header!(got, py, "REMOTE_ADDR", "192.168.1.23");
        assert_header!(got, py, "HTTP_COOKIE", "foo_language=en;");
        assert_header!(got, py, "PATH_INFO", "/foo42");
        assert_header!(got, py, "QUERY_STRING", "bar=baz");
        assert_header!(got, py, "HTTP_ACCEPT", "image/webp,*/*");
        assert_header!(
            got,
            py,
            "HTTP_ACCEPT_LANGUAGE",
            "de-DE,en-US;q=0.7,en;q=0.3"
        );
        assert_header!(got, py, "HTTP_ACCEPT_ENCODING", "gzip, deflate");
        assert_header!(got, py, "HTTP_AUTHORIZATION", "Basic YWRtaW46YWRtaW4=");
        assert_header!(got, py, "HTTP_CONNECTION", "keep-alive");
        assert_header!(got, py, "REQUEST_METHOD", "GET");
        assert_header!(got, py, "HTTP_HOST", "localhost:7878");
        assert_header!(
            got,
            py,
            "HTTP_USER_AGENT",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
        );
        assert_header!(got, py, "HTTP_DNT", "1");
        assert_header!(got, py, "SERVER_PROTOCOL", "HTTP/1.1");
    }

    #[test]
    fn test_post_simple_form() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let (g, _) = make_globals(py);
        let raw = b"POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 27\r\n\r\nfield1=value1&field2=value2";
        let mut req = WSGIRequest::new(16, String::new());
        req.append(raw);
        req.parse_data();
        let got = req.wsgi_environ(&g, py).unwrap();
        assert_header!(got, py, "CONTENT_TYPE", "application/x-www-form-urlencoded");
        let input = got
            .get_item(py, "wsgi.input")
            .unwrap()
            .as_object()
            .clone_ref(py);
        debug!("{:?}", input);
        let input = input.call_method(py, "read", NoArgs, None).unwrap();
        debug!("{:?}", input);
        assert!(input.extract::<PyBytes>(py).unwrap().data(py) == b"field1=value1&field2=value2");
    }

    #[test]
    fn test_post_multipart_formdata() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let (g, _) = make_globals(py);
        let raw = b"POST /test HTTP/1.1\r\nHost: foo.example\r\nConnection: close\r\nContent-Length: 346\r\nContent-Type: multipart/form-data; boundary=---------------------------2534525279945612714245917864\r\nDNT: 1\r\n\r\n-----------------------------2534525279945612714245917864\r\nContent-Disposition: form-data; name=\"file\"; filename=\"dummy.text\"\r\nContent-Type: text/plain\r\n\r\ndummy\r\n\r\n-----------------------------2534525279945612714245917864\r\nContent-Disposition: form-data; name=\"upload\"\r\n\r\nUpload File\r\n-----------------------------2534525279945612714245917864--\r\n";
        let mut req = WSGIRequest::new(16, String::new());
        req.append(raw);
        req.parse_data();
        let got = req.wsgi_environ(&g, py).unwrap();
        assert_header!(
            got,
            py,
            "CONTENT_TYPE",
            "multipart/form-data; boundary=---------------------------2534525279945612714245917864"
        );
        let input = got
            .get_item(py, "wsgi.input")
            .unwrap()
            .as_object()
            .clone_ref(py);
        let input = input.call_method(py, "read", NoArgs, None).unwrap();
        let expected = b"-----------------------------2534525279945612714245917864\r\nContent-Disposition: form-data; name=\"file\"; filename=\"dummy.text\"\r\nContent-Type: text/plain\r\n\r\ndummy\r\n\r\n-----------------------------2534525279945612714245917864\r\nContent-Disposition: form-data; name=\"upload\"\r\n\r\nUpload File\r\n-----------------------------2534525279945612714245917864--\r\n";
        let got = input.extract::<PyBytes>(py).unwrap();
        let got = got.data(py);
        debug!("got: {}, expected: {}", got.len(), expected.len());
        assert!(got.len() == expected.len());
        assert!(got.iter().zip(expected.iter()).all(|(p, q)| p == q));
    }

    #[test]
    fn test_get_response() {
        let mut req = WSGIRequest::new(16, String::new());
        match req.get_response() {
            None => (),
            _ => assert!(false),
        }
        let expected = b"Hello";
        let mut response = WSGIResponse::new();
        response.current_chunk = expected.to_vec();
        req.response = Arc::new(Some(response));
        match req.get_response() {
            Some(resp) => assert!(&resp.current_chunk == expected),
            _ => assert!(false),
        }
    }

    #[test]
    fn test_parsing_stages() {
        assert!(ParsingStage::HeadersSuccess.headers_complete());
        assert!(!ParsingStage::HeadersError.headers_complete());
        assert!(!ParsingStage::HeadersSuccess.complete());
        assert!(ParsingStage::ContentComplete.complete());
    }
}
