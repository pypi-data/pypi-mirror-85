use cpython::exc::{TypeError, ValueError};
use cpython::{NoArgs, ObjectProtocol, PyDict, PyErr, PyObject, PyResult, Python};
use crossbeam_channel::{unbounded, Sender};
use log::{self, set_boxed_logger, set_max_level, Level, LevelFilter, Log, Record};
pub use python3_sys::{PyGILState_Ensure, PyGILState_Release, PyGILState_STATE, Py_None};
use std::thread::spawn;

pub fn with_gil<'a, F, R>(mut code: F) -> R
where
    F: FnMut(Python<'a>, PyGILState_STATE) -> R,
{
    let (gilstate, py) = unsafe { (PyGILState_Ensure(), Python::assume_gil_acquired()) };
    let result = code(py, gilstate);
    unsafe { PyGILState_Release(gilstate) };
    result
}

pub fn with_released_gil<F, R>(gilstate: PyGILState_STATE, mut code: F) -> R
where
    F: FnMut() -> R,
{
    unsafe { PyGILState_Release(gilstate) };
    let result = code();
    unsafe { PyGILState_Ensure() };
    result
}

pub fn close_pyobject(ob: &mut PyObject, py: Python) -> PyResult<()> {
    if ob.getattr(py, "close").is_ok() {
        ob.call_method(py, "close", NoArgs, None)?;
    }
    Ok(())
}

// Notes:
//
// * Not all Python logging levels are available, only
//   those corresponding to available levels
//   in the log crate
//
// * The Rust log crate expects a global logger set *once*,
//   so it's necessary/helpful to be able to change
//   the underlying Python logger in use
fn setup_python_logger(
    py: Python,
    name: &str,
) -> PyResult<(u8, u8, u8, u8, PyObject, LevelFilter)> {
    let locals = PyDict::new(py);
    let pylogging = py.import("logging")?;
    let crit = pylogging.get(py, "CRITICAL")?.extract(py)?;
    let debug = pylogging.get(py, "DEBUG")?.extract(py)?;
    let error = pylogging.get(py, "ERROR")?.extract(py)?;
    let info = pylogging.get(py, "INFO")?.extract(py)?;
    let warn = pylogging.get(py, "WARN")?.extract(py)?;
    locals.set_item(py, "logging", pylogging)?;
    let logger: PyObject = py
        .eval(
            &format!("logging.getLogger('{}')", name),
            None,
            Some(&locals),
        )?
        .extract(py)?;
    let level = logger.call_method(py, "getEffectiveLevel", NoArgs, None)?;
    match level.extract::<u8>(py) {
        Ok(u8lvl) => {
            let filter = match u8lvl {
                lvl if lvl == crit => LevelFilter::Error,
                lvl if lvl == debug => LevelFilter::Trace,
                lvl if lvl == error => LevelFilter::Error,
                lvl if lvl == info => LevelFilter::Info,
                lvl if lvl == warn => LevelFilter::Warn,
                _ => LevelFilter::Off,
            };
            set_max_level(filter);
            Ok((debug, error, info, warn, logger, filter))
        }
        Err(_) => Err(PyErr::new::<TypeError, _>(
            py,
            format!("Expected u8, got {:?}", level),
        )),
    }
}

pub struct SyncPythonLogger {
    logger: PyObject,
    debug: u8,
    error: u8,
    info: u8,
    warn: u8,
    level: Option<Level>,
}

impl SyncPythonLogger {
    pub fn new(py: Python, name: &str) -> PyResult<Self> {
        match setup_python_logger(py, name) {
            Ok((debug, error, info, warn, logger, filter)) => Ok(Self {
                logger,
                debug,
                error,
                info,
                warn,
                level: filter.to_level(),
            }),
            Err(e) => Err(e),
        }
    }

    fn python_level(&self, level: Level) -> u8 {
        match level {
            Level::Error => self.error,
            Level::Warn => self.warn,
            Level::Info => self.info,
            Level::Debug => self.debug,
            Level::Trace => self.debug,
        }
    }
}

impl Log for SyncPythonLogger {
    fn enabled(&self, metadata: &log::Metadata) -> bool {
        self.level.map_or(false, |lvl| metadata.level() <= lvl)
    }

    fn log(&self, record: &Record) {
        with_gil(|py, _gs| {
            if self
                .logger
                .call_method(
                    py,
                    "log",
                    (
                        self.python_level(record.level()),
                        format!("{}", record.args()),
                    ),
                    None,
                )
                .is_err()
            {
                PyErr::fetch(py);
            }
        });
    }

    fn flush(&self) {}
}

pub struct AsyncPythonLogger {
    records: Sender<(u8, String)>,
    debug: u8,
    error: u8,
    info: u8,
    warn: u8,
    level: Option<Level>,
}

impl AsyncPythonLogger {
    const STOPMARKER: (u8, String) = (99, String::new());

    pub fn new(py: Python, name: &str) -> PyResult<Self> {
        match setup_python_logger(py, name) {
            Ok((debug, error, info, warn, logger, filter)) => {
                let records = Self::create_logging_thread(logger);
                Ok(Self {
                    records,
                    debug,
                    error,
                    info,
                    warn,
                    level: filter.to_level(),
                })
            }
            Err(e) => Err(e),
        }
    }

    fn python_level(&self, level: Level) -> u8 {
        match level {
            Level::Error => self.error,
            Level::Warn => self.warn,
            Level::Info => self.info,
            Level::Debug => self.debug,
            Level::Trace => self.debug,
        }
    }

    fn create_logging_thread(pylog: PyObject) -> Sender<(u8, String)> {
        let (tx, rx) = unbounded();
        spawn(move || {
            while let Ok(record) = rx.recv() {
                if record == Self::STOPMARKER {
                    break;
                }
                with_gil(|py, _gs| {
                    if pylog.call_method(py, "log", &record, None).is_err() {
                        PyErr::fetch(py);
                    }
                });
            }
        });
        tx
    }
}

impl Log for AsyncPythonLogger {
    fn enabled(&self, metadata: &log::Metadata) -> bool {
        self.level.map_or(false, |lvl| metadata.level() <= lvl)
    }

    fn log(&self, record: &Record) {
        self.records
            .send((
                self.python_level(record.level()),
                format!("{}", record.args()),
            ))
            .unwrap();
    }

    fn flush(&self) {}
}

impl Drop for AsyncPythonLogger {
    fn drop(&mut self) {
        if self.records.send(Self::STOPMARKER).is_err() {}
    }
}

macro_rules! set_global_python_logger {
    ($L: ident, $py: ident, $name: ident) => {
        match $L::new($py, $name) {
            Ok(logging) => match set_boxed_logger(Box::new(logging)) {
                Ok(_) => Ok(()),
                Err(_) => Err(PyErr::new::<ValueError, _>(
                    $py,
                    format!("Logging already initialized"),
                )),
            },
            Err(e) => Err(e),
        }
    };
}

pub fn async_logger(py: Python, name: &str) -> PyResult<()> {
    set_global_python_logger!(AsyncPythonLogger, py, name)
}

pub fn sync_logger(py: Python, name: &str) -> PyResult<()> {
    set_global_python_logger!(SyncPythonLogger, py, name)
}

#[cfg(test)]
mod tests {
    use cpython::{PyDict, Python};
    use log::{max_level, Level, LevelFilter, Log, Record};
    use python3_sys::{PyEval_RestoreThread, PyEval_SaveThread};
    use std::fs::{remove_file, File};
    use std::io::Read;
    use std::{thread, time};

    use crate::pyutils::{with_gil, AsyncPythonLogger, SyncPythonLogger};

    #[test]
    fn test_async_logging() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
import logging
from tempfile import mkstemp

_, logfilename = mkstemp()

# create logger
logger = logging.getLogger('foo')
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
handler = logging.FileHandler(logfilename)
handler.setFormatter(fmt)
logger.addHandler(handler)"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => match AsyncPythonLogger::new(py, "foo") {
                Ok(logger) => {
                    assert_eq!(max_level(), LevelFilter::Trace);
                    let py_thread_state = unsafe { PyEval_SaveThread() };
                    with_gil(|_py, _gs| {
                        let record = Record::builder()
                            .args(format_args!("debug: foo"))
                            .level(Level::Debug)
                            .target("pyruvate")
                            .file(Some("pyutils.rs"))
                            .line(Some(23))
                            .module_path(Some("tests"))
                            .build();
                        assert!(logger.enabled(record.metadata()));
                        logger.log(&record);
                        let record = Record::builder()
                            .args(format_args!("Foo error encountered"))
                            .level(Level::Error)
                            .target("pyruvate")
                            .file(Some("pyutils.rs"))
                            .line(Some(23))
                            .module_path(Some("tests"))
                            .build();
                        assert!(logger.enabled(record.metadata()));
                        logger.log(&record);
                        let record = Record::builder()
                            .args(format_args!("bar baz info"))
                            .level(Level::Info)
                            .target("pyruvate")
                            .file(Some("pyutils.rs"))
                            .line(Some(23))
                            .module_path(Some("tests"))
                            .build();
                        assert!(logger.enabled(record.metadata()));
                        logger.log(&record);
                        let record = Record::builder()
                            .args(format_args!("tracing foo ..."))
                            .level(Level::Trace)
                            .target("pyruvate")
                            .file(Some("pyutils.rs"))
                            .line(Some(23))
                            .module_path(Some("tests"))
                            .build();
                        assert!(logger.enabled(record.metadata()));
                        logger.log(&record);
                        let record = Record::builder()
                            .args(format_args!("there's a foo!"))
                            .level(Level::Warn)
                            .target("pyruvate")
                            .file(Some("pyutils.rs"))
                            .line(Some(23))
                            .module_path(Some("tests"))
                            .build();
                        assert!(logger.enabled(record.metadata()));
                        logger.log(&record);
                    });
                    // yield
                    thread::sleep(time::Duration::from_millis(10));
                    unsafe { PyEval_RestoreThread(py_thread_state) };
                    let logfilename: String = locals
                        .get_item(py, "logfilename")
                        .unwrap()
                        .extract(py)
                        .unwrap();
                    let mut logfile = File::open(&logfilename).unwrap();
                    let mut contents = String::new();
                    logfile.read_to_string(&mut contents).unwrap();
                    assert_eq!("DEBUG:foo:debug: foo\nERROR:foo:Foo error encountered\nINFO:foo:bar baz info\nDEBUG:foo:tracing foo ...\nWARNING:foo:there's a foo!\n", contents);
                    remove_file(logfilename).unwrap();
                }
                Err(_) => assert!(false),
            },
            Err(e) => {
                println!("Error: {:?}", e);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_sync_logging() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
import logging
from tempfile import mkstemp

_, logfilename = mkstemp()

# create logger
logger = logging.getLogger('foo')
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
handler = logging.FileHandler(logfilename)
handler.setFormatter(fmt)
logger.addHandler(handler)"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => match SyncPythonLogger::new(py, "foo") {
                Ok(logger) => {
                    assert_eq!(max_level(), LevelFilter::Trace);
                    let py_thread_state = unsafe { PyEval_SaveThread() };
                    let record = Record::builder()
                        .args(format_args!("debug: foo"))
                        .level(Level::Debug)
                        .target("pyruvate")
                        .file(Some("pyutils.rs"))
                        .line(Some(23))
                        .module_path(Some("tests"))
                        .build();
                    assert!(logger.enabled(record.metadata()));
                    logger.log(&record);
                    let record = Record::builder()
                        .args(format_args!("Foo error encountered"))
                        .level(Level::Error)
                        .target("pyruvate")
                        .file(Some("pyutils.rs"))
                        .line(Some(23))
                        .module_path(Some("tests"))
                        .build();
                    assert!(logger.enabled(record.metadata()));
                    logger.log(&record);
                    let record = Record::builder()
                        .args(format_args!("bar baz info"))
                        .level(Level::Info)
                        .target("pyruvate")
                        .file(Some("pyutils.rs"))
                        .line(Some(23))
                        .module_path(Some("tests"))
                        .build();
                    assert!(logger.enabled(record.metadata()));
                    logger.log(&record);
                    let record = Record::builder()
                        .args(format_args!("tracing foo ..."))
                        .level(Level::Trace)
                        .target("pyruvate")
                        .file(Some("pyutils.rs"))
                        .line(Some(23))
                        .module_path(Some("tests"))
                        .build();
                    assert!(logger.enabled(record.metadata()));
                    logger.log(&record);
                    let record = Record::builder()
                        .args(format_args!("there's a foo!"))
                        .level(Level::Warn)
                        .target("pyruvate")
                        .file(Some("pyutils.rs"))
                        .line(Some(23))
                        .module_path(Some("tests"))
                        .build();
                    assert!(logger.enabled(record.metadata()));
                    logger.log(&record);
                    let logfilename: String = locals
                        .get_item(py, "logfilename")
                        .unwrap()
                        .extract(py)
                        .unwrap();
                    unsafe { PyEval_RestoreThread(py_thread_state) };
                    let mut logfile = File::open(&logfilename).unwrap();
                    let mut contents = String::new();
                    logfile.read_to_string(&mut contents).unwrap();
                    assert_eq!("DEBUG:foo:debug: foo\nERROR:foo:Foo error encountered\nINFO:foo:bar baz info\nDEBUG:foo:tracing foo ...\nWARNING:foo:there's a foo!\n", contents);
                    remove_file(logfilename).unwrap();
                }
                Err(_) => assert!(false),
            },
            Err(e) => {
                println!("Error: {:?}", e);
                assert!(false);
            }
        }
    }
}
