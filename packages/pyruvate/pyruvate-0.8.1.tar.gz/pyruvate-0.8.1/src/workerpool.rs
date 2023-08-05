use cpython::{PyClone, PyObject, Python};
use crossbeam_channel::{unbounded, Receiver, SendError, Sender};
use mio::Token;
use threadpool::ThreadPool;

use crate::request::WSGIRequest;
use crate::transport::Socket;

pub const MARKER: Token = Token(0);
type SendResult<T> = Result<(), SendError<(Token, (WSGIRequest, Option<T>))>>;

pub struct WorkerPool<T: Socket> {
    workers: ThreadPool,
    application: PyObject,
    input: Sender<(Token, (WSGIRequest, Option<T>))>,
}

impl<T: 'static + Socket> WorkerPool<T> {
    pub fn new<F>(
        server_name: String,
        server_port: String,
        script_name: String,
        application: PyObject,
        worker: F,
        num_workers: usize,
        py: Python,
    ) -> WorkerPool<T>
    where
        F: 'static
            + Fn(usize, String, String, PyObject, String, Receiver<(Token, (WSGIRequest, Option<T>))>)
            + Send
            + Copy,
    {
        let (input, rcv) = unbounded::<(Token, (WSGIRequest, Option<T>))>();
        let wp = WorkerPool {
            application,
            workers: ThreadPool::new(num_workers),
            input,
        };
        for idx in 0..num_workers {
            let rcv = rcv.clone();
            let threadapp = wp.application.clone_ref(py); // "Clone self, Calls Py_INCREF() on the ptr."
            let sn = script_name.clone();
            let sip = server_name.clone();
            let sp = server_port.clone();
            wp.workers.execute(move || {
                worker(idx, sip, sp, threadapp, sn, rcv);
            });
        }
        wp
    }

    pub fn execute(&mut self, token: Token, req: WSGIRequest, out: Option<T>) -> SendResult<T> {
        self.input.send((token, (req, out)))
    }

    pub fn join(&mut self) -> SendResult<T> {
        for _ in 0..self.workers.max_count() {
            self.execute(MARKER, WSGIRequest::new(0, String::new()), None)?;
        }
        self.workers.join();
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use cpython::{PyClone, PyDict, Python, PythonObject};
    use log::debug;
    use mio::net::{TcpListener, TcpStream};
    use mio::Token;
    use python3_sys::{PyEval_RestoreThread, PyEval_SaveThread};

    use crate::request::WSGIRequest;
    use crate::workerpool::WorkerPool;
    use crate::workers::{write_blocking_worker, write_non_blocking_worker};

    #[test]
    fn test_pool_simple_blocking() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let server_name = String::from("127.0.0.1");
        let port = String::from("0");
        let sn = "/foo";
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
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
                let mut req1 = WSGIRequest::new(16, String::new());
                req1.append(raw);
                req1.parse_data();
                let mut req2 = WSGIRequest::new(16, String::new());
                req2.append(raw);
                req2.parse_data();
                let mut req3 = WSGIRequest::new(16, String::new());
                req3.append(raw);
                req3.parse_data();
                let mut req4 = WSGIRequest::new(16, String::new());
                req4.append(raw);
                req4.parse_data();
                let mut wp = WorkerPool::<TcpStream>::new(
                    server_name,
                    port,
                    sn.to_string(),
                    app,
                    write_blocking_worker::<TcpListener, TcpStream>,
                    2,
                    py,
                );
                let token = Token(42);
                let py_thread_state = unsafe { PyEval_SaveThread() };
                wp.execute(token, req1, None).unwrap();
                wp.execute(token, req2, None).unwrap();
                wp.execute(token, req3, None).unwrap();
                wp.execute(token, req4, None).unwrap();
                match wp.join() {
                    Ok(_) => debug!("wp joined"),
                    Err(_) => {
                        debug!("Could not join workers");
                        assert!(false);
                    }
                }
                unsafe { PyEval_RestoreThread(py_thread_state) };
            }
            Err(e) => {
                debug!("Error encountered: {:?}", e);
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_pool_simple_non_blocking() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let server_name = String::from("127.0.0.1");
        let port = String::from("0");
        let sn = "/foo";
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
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
                let mut req1 = WSGIRequest::new(16, String::new());
                req1.append(raw);
                req1.parse_data();
                let mut req2 = WSGIRequest::new(16, String::new());
                req2.append(raw);
                req2.parse_data();
                let mut req3 = WSGIRequest::new(16, String::new());
                req3.append(raw);
                req3.parse_data();
                let mut req4 = WSGIRequest::new(16, String::new());
                req4.append(raw);
                req4.parse_data();
                let mut wp = WorkerPool::<TcpStream>::new(
                    server_name,
                    port,
                    sn.to_string(),
                    app,
                    write_non_blocking_worker::<TcpListener, TcpStream>,
                    2,
                    py,
                );
                let token = Token(42);
                let py_thread_state = unsafe { PyEval_SaveThread() };
                wp.execute(token, req1, None).unwrap();
                wp.execute(token, req2, None).unwrap();
                wp.execute(token, req3, None).unwrap();
                wp.execute(token, req4, None).unwrap();
                match wp.join() {
                    Ok(_) => debug!("wp joined"),
                    Err(_) => {
                        debug!("Could not join workers");
                        assert!(false);
                    }
                }
                unsafe { PyEval_RestoreThread(py_thread_state) };
            }
            Err(e) => {
                debug!("Error encountered: {:?}", e);
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }
}
