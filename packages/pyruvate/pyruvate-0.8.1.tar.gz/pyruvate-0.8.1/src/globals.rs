use cpython::{PyDict, PyErr, PyModule, PyResult, PyString, Python};
use log::{debug, error};

pub struct WSGIGlobals<'a> {
    pub server_name: &'a str,
    pub server_port: &'a str,
    pub script_name: &'a str,
    pub io_module: PyModule,
    pub sys_module: PyModule,
    pub wsgi_module: Option<PyModule>,
    pub wsgi_environ: PyDict,
    pub peer_addr_key: PyString,
    pub content_length_key: PyString,
    pub wsgi_input_key: PyString,
}

impl<'a> WSGIGlobals<'a> {
    pub fn new(
        server_name: &'a str,
        server_port: &'a str,
        script_name: &'a str,
        py: Python,
    ) -> WSGIGlobals<'a> {
        // XXX work around not being able to import wsgi module from tests
        let wsgi_module = match py.import("pyruvate") {
            Ok(pyruvate) => Some(pyruvate),
            Err(_) => {
                error!("Could not import WSGI module, so no FileWrapper");
                PyErr::fetch(py);
                None
            }
        };
        let sys_module = py.import("sys").expect("Could not import module sys");
        let wsgi_environ = Self::prepare_wsgi_environ(
            server_name,
            server_port,
            script_name,
            &sys_module,
            wsgi_module.as_ref(),
            py,
        )
        .expect("Could not create wsgi environ template");
        WSGIGlobals {
            server_name,
            server_port,
            script_name,
            io_module: py.import("io").expect("Could not import module io"),
            sys_module,
            wsgi_module,
            wsgi_environ,
            peer_addr_key: PyString::new(py, "REMOTE_ADDR"),
            content_length_key: PyString::new(py, "CONTENT_LENGTH"),
            wsgi_input_key: PyString::new(py, "wsgi.input"),
        }
    }

    fn prepare_wsgi_environ(
        server_name: &'a str,
        server_port: &'a str,
        script_name: &'a str,
        sys: &PyModule,
        wsgi: Option<&PyModule>,
        py: Python,
    ) -> PyResult<PyDict> {
        let environ = PyDict::new(py);
        environ.set_item(py, "SERVER_NAME", server_name)?;
        environ.set_item(py, "SERVER_PORT", server_port)?;
        environ.set_item(py, "SCRIPT_NAME", script_name)?;
        environ.set_item(py, "wsgi.errors", sys.get(py, "stderr")?)?;
        environ.set_item(py, "wsgi.version", (1, 0))?;
        environ.set_item(py, "wsgi.multithread", false)?;
        environ.set_item(py, "wsgi.multiprocess", true)?;
        environ.set_item(py, "wsgi.run_once", false)?;
        environ.set_item(py, "wsgi.url_scheme", "http")?;
        if let Some(wsgi) = wsgi {
            debug!("Setting FileWrapper in environ");
            environ.set_item(py, "wsgi.file_wrapper", wsgi.get(py, "FileWrapper")?)?;
        }
        Ok(environ)
    }
}

#[cfg(test)]
mod tests {
    use crate::globals::WSGIGlobals;
    use cpython::Python;
    use log::debug;

    #[test]
    fn test_creation() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let sn = "127.0.0.1";
        let sp = "7878";
        let script = "/foo";
        let pypath = py.import("sys").unwrap().get(py, "path").unwrap();
        debug!("sys.path: {:?}", pypath);
        let got = WSGIGlobals::new(sn, sp, script, py);
        assert!(got.server_name == sn);
        assert!(got.server_port == sp);
        assert!(got.script_name == script);
    }
}
