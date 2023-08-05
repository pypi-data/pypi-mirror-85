use cpython::exc::{IOError, ValueError};
use cpython::{PyErr, PyObject, PyResult, Python};
use mio::net::{TcpListener, UnixListener};
use std::net::SocketAddr;

use crate::filewrapper::FileWrapper;
use crate::globals::WSGIGlobals;
use crate::pyutils::{async_logger, sync_logger};
use crate::server::Server;
use crate::startresponse::StartResponse;
use crate::transport::{parse_server_info, SocketActivation};

macro_rules! server_loop {
    ($L:ty, $application: ident, $globals: ident, $listener: ident, $num_workers: ident, $write_blocking: ident, $max_number_headers: ident, $async_logging: ident, $py: ident) => {
        match Server::<$L>::new(
            $application,
            &$globals,
            $listener,
            $num_workers,
            $write_blocking,
            $max_number_headers,
            $py,
        ) {
            Ok(mut server) => {
                let res = if $async_logging {
                    async_logger($py, "pyruvate")
                } else {
                    sync_logger($py, "pyruvate")
                };
                match res {
                    Ok(_) => match server.serve() {
                        Ok(_) => Ok($py.None()),
                        Err(_) => Err(PyErr::new::<IOError, _>(
                            $py,
                            "Error encountered during event loop",
                        )),
                    },
                    Err(_) => Err(PyErr::new::<IOError, _>($py, "Could not setup logging")),
                }
            }
            Err(e) => Err(PyErr::new::<IOError, _>(
                $py,
                format!("Could not create server: {:?}", e),
            )),
        }
    };
}

fn serve(
    py: Python,
    application: PyObject,
    addr: Option<String>,
    num_workers: usize,
    write_blocking: bool,
    max_number_headers: usize,
    async_logging: bool,
) -> PyResult<PyObject> {
    if num_workers < 1 {
        return Err(PyErr::new::<ValueError, _>(py, "Need at least 1 worker"));
    }
    let (server_name, server_port) = match &addr {
        Some(addr) => parse_server_info(&addr),
        None => (String::new(), String::new()),
    };
    let globals = WSGIGlobals::new(&server_name, &server_port, "", py);
    match addr {
        Some(addr) => {
            match addr.parse::<SocketAddr>() {
                Ok(sockaddr) => match TcpListener::bind(sockaddr) {
                    Ok(listener) => server_loop!(
                        TcpListener,
                        application,
                        globals,
                        listener,
                        num_workers,
                        write_blocking,
                        max_number_headers,
                        async_logging,
                        py
                    ),
                    Err(e) => {
                        println!("Error binding socket: {:?}", e);
                        Err(PyErr::new::<IOError, _>(
                            py,
                            format!("Could not bind socket: {:?}", e),
                        ))
                    }
                },
                Err(_) => {
                    // fallback to UnixListener
                    match UnixListener::bind(addr) {
                        Ok(listener) => server_loop!(
                            UnixListener,
                            application,
                            globals,
                            listener,
                            num_workers,
                            write_blocking,
                            max_number_headers,
                            async_logging,
                            py
                        ),
                        Err(e) => Err(PyErr::new::<IOError, _>(
                            py,
                            format!("Could not bind unix domain socket: {:?}", e),
                        )),
                    }
                }
            }
        }
        // try systemd socket activation
        None => match TcpListener::from_active_socket() {
            Ok(listener) => server_loop!(
                TcpListener,
                application,
                globals,
                listener,
                num_workers,
                write_blocking,
                max_number_headers,
                async_logging,
                py
            ),
            Err(_) => {
                // fall back to UnixListener
                match UnixListener::from_active_socket() {
                    Ok(listener) => server_loop!(
                        UnixListener,
                        application,
                        globals,
                        listener,
                        num_workers,
                        write_blocking,
                        max_number_headers,
                        async_logging,
                        py
                    ),
                    Err(e) => Err(PyErr::new::<IOError, _>(
                        py,
                        format!("Socket activation: {}", e),
                    )),
                }
            }
        },
    }
}

py_module_initializer!(pyruvate, initpyruvate, PyInit_pyruvate, |py, m| {
    m.add(py, "__doc__", "Pyruvate WSGI server")
        .expect("Could not add documentation string");
    m.add_class::<StartResponse>(py)
        .expect("Could not add StartResponse class to module");
    m.add_class::<FileWrapper>(py)
        .expect("Could not add FileWrapper class to module");
    m.add(
        py,
        "serve",
        py_fn!(
            py,
            serve(
                application: PyObject,
                addr: Option<String> = None,
                num_workers: usize = 2,
                write_blocking: bool = false,
                max_number_headers: usize = 24,
                async_logging: bool = true,
            )
        ),
    )
    .expect("Could not add serve() function to module");
    Ok(())
});
