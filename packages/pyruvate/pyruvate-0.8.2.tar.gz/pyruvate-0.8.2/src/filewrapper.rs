#![allow(clippy::transmute_ptr_to_ptr, clippy::zero_ptr)] // suppress warnings in py_class invocation
use cpython::{
    NoArgs, ObjectProtocol, PyObject, PyResult, PyTuple, Python, PythonObject, ToPyObject,
};
use errno::errno;
use log::{debug, error};
use std::cell::RefCell;
use std::cmp;
use std::io::Error;
use std::os::unix::io::{AsRawFd, RawFd};

use crate::pyutils::{close_pyobject, with_released_gil, PyGILState_STATE};
use crate::transport::would_block;

// This is the maximum the Linux kernel will write in a single sendfile call.
const SENDFILE_MAXSIZE: isize = 0x7fff_f000;

pub struct SendFileInfo {
    pub content_length: isize,
    pub blocksize: isize,
    pub offset: libc::off_t,
    pub fd: RawFd,
    pub done: bool,
}

impl SendFileInfo {
    pub fn new(fd: RawFd, blocksize: isize) -> Self {
        Self {
            content_length: -1,
            blocksize,
            offset: 0,
            fd,
            done: false,
        }
    }

    // true: chunk written completely, false: there's more
    pub fn send_file(&mut self, out: &mut dyn AsRawFd) -> bool {
        debug!("Sending file");
        let mut count = if self.blocksize < 0 {
            SENDFILE_MAXSIZE
        } else {
            self.blocksize
        };
        if self.content_length >= 0 {
            count = cmp::min(self.content_length - self.offset as isize, count);
        }
        self.done = (count == 0) || {
            match unsafe {
                libc::sendfile(out.as_raw_fd(), self.fd, &mut self.offset, count as usize)
            } {
                -1 => {
                    // will cover the case where count is too large as EOVERFLOW
                    // s. sendfile(2)
                    let err = Error::from(errno());
                    if !would_block(&err) {
                        error!("Could not sendfile(): {:?}", err);
                        true
                    } else {
                        false
                    }
                }
                // 0 bytes written, assuming we're done
                0 => true,
                _ if (self.content_length > 0) => self.content_length == self.offset as isize,
                // If no content length is given, num_written might be less than count.
                // However the subsequent call will write 0 bytes -> done.
                _ => false,
            }
        };
        self.done
    }

    fn update_content_length(&mut self, content_length: isize) {
        self.content_length = content_length;
        if self.blocksize > content_length {
            self.blocksize = content_length;
        }
    }
}

impl Iterator for SendFileInfo {
    type Item = Vec<u8>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.done {
            None
        } else {
            Some(Vec::new())
        }
    }
}

py_class!(pub class FileWrapper |py| {
    data filelike: RefCell<PyObject>;
    data sendfileinfo: RefCell<SendFileInfo>;

    def __new__(_cls, filelike: PyObject, blocksize: Option<isize>=None) -> PyResult<Self> {
        let mut filelike = RefCell::new(filelike);
        let blocksize = match blocksize {
            Some(bs) => bs,
            None => -1
        };
        let mut fd: RawFd = -1;
        if let Ok(fdpyob) = filelike.get_mut().call_method(py, "fileno", NoArgs, None) {
            if let Ok(pyfd) = fdpyob.extract(py) {
                fd = pyfd;
            }
        };
        let sendfileinfo = RefCell::new(SendFileInfo::new(fd, blocksize));
        FileWrapper::create_instance(py, filelike, sendfileinfo)
    }

    def close(&self) -> PyResult<PyObject> {
        match close_pyobject(&mut self.filelike(py).borrow_mut(), py) {
            Ok(_) => Ok(py.None()),
            Err(e) => Err(e)
        }
    }

});

pub trait SendFile {
    // Put this in a trait for more flexibility.
    fn sendfileinfo<'p>(&'p self, py: Python<'p>) -> &'p RefCell<SendFileInfo>;
    fn send_file(&mut self, out: &mut dyn AsRawFd, gilstate: PyGILState_STATE, py: Python) -> bool;
    fn update_content_length(&mut self, content_length: usize, py: Python);
    // XXX used only for testing
    fn new(py: Python, fd: RawFd, bs: isize) -> PyResult<FileWrapper>;
}

impl SendFile for FileWrapper {
    // public getter
    fn sendfileinfo<'p>(&'p self, py: Python<'p>) -> &'p RefCell<SendFileInfo> {
        self.sendfileinfo(py)
    }

    fn send_file(&mut self, out: &mut dyn AsRawFd, gilstate: PyGILState_STATE, py: Python) -> bool {
        with_released_gil(gilstate, || {
            self.sendfileinfo(py).borrow_mut().send_file(out)
        })
    }

    fn update_content_length(&mut self, content_length: usize, py: Python) {
        self.sendfileinfo(py)
            .borrow_mut()
            .update_content_length(content_length as isize);
    }

    fn new(py: Python, fd: RawFd, bs: isize) -> PyResult<FileWrapper> {
        FileWrapper::create_instance(
            py,
            RefCell::new(py.None()),
            RefCell::new(SendFileInfo::new(fd, bs)),
        )
    }
}

impl Iterator for FileWrapper {
    type Item = Vec<u8>;

    fn next(&mut self) -> Option<Self::Item> {
        let py = unsafe { Python::assume_gil_acquired() };
        if self.sendfileinfo(py).borrow().fd != -1 {
            return self.sendfileinfo(py).borrow_mut().next();
        }
        match self.filelike(py).borrow_mut().call_method(
            py,
            "read",
            PyTuple::new(
                py,
                &[self
                    .sendfileinfo(py)
                    .borrow()
                    .blocksize
                    .to_py_object(py)
                    .into_object()],
            ),
            None,
        ) {
            Ok(bytes) => {
                if bytes != py.None() {
                    match bytes.extract::<Vec<u8>>(py) {
                        Ok(result) => {
                            if !result.is_empty() {
                                Some(result)
                            } else {
                                None
                            }
                        }
                        Err(e) => {
                            debug!("Could not extract from bytes");
                            e.print_and_set_sys_last_vars(py);
                            None
                        }
                    }
                } else {
                    None
                }
            }
            Err(e) => {
                debug!("Fileno: {}", self.sendfileinfo(py).borrow().fd);
                e.print_and_set_sys_last_vars(py);
                None
            }
        }
    }
}

#[cfg(test)]
mod tests {

    use cpython::exc::TypeError;
    use cpython::{
        NoArgs, ObjectProtocol, PyClone, PyDict, PyErr, PyTuple, Python, PythonObject, ToPyObject,
    };
    use std::io::{Read, Seek, Write};
    use std::net::{SocketAddr, TcpListener, TcpStream};
    use std::os::unix::io::{AsRawFd, RawFd};
    use std::sync::mpsc::channel;
    use std::thread;
    use tempfile::NamedTempFile;

    use crate::filewrapper::{FileWrapper, SendFile};

    #[test]
    fn test_no_fileno() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def fileno(self):
        return -1

    def read(self, blocksize):
        result = b'Foo 42'[self.offset:self.offset+blocksize]
        self.offset += blocksize
        return result

f = FL()"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let filelike = locals
                    .get_item(py, "f")
                    .expect("Could not get file object")
                    .as_object()
                    .clone_ref(py);
                let fd: RawFd = filelike
                    .call_method(py, "fileno", NoArgs, None)
                    .expect("Could not call fileno method")
                    .extract(py)
                    .expect("Could not extract RawFd");
                let fwtype = py.get_type::<FileWrapper>();
                let bs: i32 = 2;
                let fwany = fwtype
                    .call(
                        py,
                        PyTuple::new(
                            py,
                            &[filelike, bs.to_py_object(py).as_object().clone_ref(py)],
                        ),
                        None,
                    )
                    .unwrap();
                if let Ok(mut fw) = fwany.extract::<FileWrapper>(py) {
                    assert_eq!(fw.sendfileinfo(py).borrow().fd, fd);
                    for chunk in vec![b"Fo", b"o ", b"42"] {
                        match fw.next() {
                            Some(got) => {
                                assert_eq!(chunk, &got[..]);
                            }
                            None => {
                                assert!(false);
                            }
                        }
                    }
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
    fn test_no_read_method() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def fileno(self):
        return -1

f = FL()"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let filelike = locals
                    .get_item(py, "f")
                    .expect("Could not get file object")
                    .as_object()
                    .clone_ref(py);
                let fwtype = py.get_type::<FileWrapper>();
                let bs: i32 = 2;
                let fwany = fwtype
                    .call(
                        py,
                        PyTuple::new(
                            py,
                            &[filelike, bs.to_py_object(py).as_object().clone_ref(py)],
                        ),
                        None,
                    )
                    .unwrap();
                if let Ok(mut fw) = fwany.extract::<FileWrapper>(py) {
                    match fw.next() {
                        Some(_) => {
                            assert!(false);
                        }
                        None => {
                            assert!(true);
                        }
                    }
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
    fn test_bytes_not_convertible() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let locals = PyDict::new(py);
        match py.run(
            r#"
class FL(object):

    def __init__(self):
        self.offset = 0

    def read(self, blocksize):
        result = 'öäü'
        self.offset += blocksize
        return result

    def fileno(self):
        return -1

f = FL()"#,
            None,
            Some(&locals),
        ) {
            Ok(_) => {
                let filelike = locals
                    .get_item(py, "f")
                    .expect("Could not get file object")
                    .as_object()
                    .clone_ref(py);
                let fwtype = py.get_type::<FileWrapper>();
                let bs: i32 = 2;
                let fwany = fwtype
                    .call(
                        py,
                        PyTuple::new(
                            py,
                            &[filelike, bs.to_py_object(py).as_object().clone_ref(py)],
                        ),
                        None,
                    )
                    .unwrap();
                if let Ok(mut fw) = fwany.extract::<FileWrapper>(py) {
                    match fw.next() {
                        Some(_) => {
                            assert!(false);
                        }
                        None => {
                            assert!(true);
                        }
                    }
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
    fn test_send_file() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr: SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let mut tmp = NamedTempFile::new().unwrap();
        let mut f = tmp.reopen().unwrap();
        f.seek(std::io::SeekFrom::Start(0)).unwrap();
        let fw = FileWrapper::new(py, f.as_raw_fd(), 4).unwrap();
        tmp.write_all(b"Hello World!\n").unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 13];
            let snd = snd.clone();
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        let mut sfi = fw.sendfileinfo(py).borrow_mut();
        let empty: Option<Vec<u8>> = Some(Vec::new());
        sfi.send_file(&mut connection);
        let mut b = got.recv().unwrap();
        assert_eq!(&b[..], b"Hell\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 4);
        assert_eq!(sfi.next(), empty);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        assert_eq!(&b[..], b"o Wo\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 8);
        assert_eq!(sfi.next(), empty);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        assert_eq!(&b[..], b"rld!\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 12);
        assert_eq!(sfi.next(), empty);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        assert_eq!(&b[..], b"\n\0\0\0\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 13);
        // no content length + blocksize > number bytes written, next should yield some
        assert_eq!(sfi.next(), empty);
        sfi.send_file(&mut connection);
        assert_eq!(sfi.next(), None);
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_send_file_updated_content_length() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr: SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let mut tmp = NamedTempFile::new().unwrap();
        let mut f = tmp.reopen().unwrap();
        f.seek(std::io::SeekFrom::Start(0)).unwrap();
        let mut fw = FileWrapper::new(py, f.as_raw_fd(), 4).unwrap();
        fw.update_content_length(5, py);
        tmp.write_all(b"Hello World!\n").unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 13];
            let snd = snd.clone();
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            buf = [0; 13];
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        let mut sfi = fw.sendfileinfo(py).borrow_mut();
        sfi.send_file(&mut connection);
        let mut b = got.recv().unwrap();
        let empty: Option<Vec<u8>> = Some(Vec::new());
        assert_eq!(&b[..], b"Hell\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 4);
        assert_eq!(sfi.next(), empty);
        sfi.send_file(&mut connection);
        b = got.recv().unwrap();
        assert_eq!(&b[..], b"o\0\0\0\0\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 5);
        assert_eq!(sfi.next(), None);
        sfi.send_file(&mut connection);
        assert_eq!(sfi.next(), None);
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_send_file_content_length_lt_blocksize() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let addr: SocketAddr = "127.0.0.1:0".parse().expect("Failed to parse address");
        let server = TcpListener::bind(addr).expect("Failed to bind address");
        let addr = server.local_addr().unwrap();
        let mut tmp = NamedTempFile::new().unwrap();
        let mut f = tmp.reopen().unwrap();
        f.seek(std::io::SeekFrom::Start(0)).unwrap();
        let mut fw = FileWrapper::new(py, f.as_raw_fd(), 7).unwrap();
        fw.update_content_length(5, py);
        let mut sfi = fw.sendfileinfo(py).borrow_mut();
        assert_eq!(sfi.blocksize, 5);
        tmp.write_all(b"Hello World!\n").unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        let t = thread::spawn(move || {
            let (mut conn, _addr) = server.accept().unwrap();
            let mut buf = [0; 13];
            let snd = snd.clone();
            conn.read(&mut buf).unwrap();
            snd.send(buf).unwrap();
            rx.recv().unwrap();
        });
        let mut connection = TcpStream::connect(addr).expect("Failed to connect");
        sfi.send_file(&mut connection);
        let b = got.recv().unwrap();
        assert_eq!(&b[..], b"Hello\0\0\0\0\0\0\0\0");
        assert_eq!(sfi.offset, 5);
        assert_eq!(sfi.next(), None);
        sfi.send_file(&mut connection);
        assert_eq!(sfi.next(), None);
        tx.send(()).unwrap();
        t.join().unwrap();
    }

    #[test]
    fn test_file_wrapper_new_no_args() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let fwtype = py.get_type::<FileWrapper>();
        match fwtype.call(py, PyTuple::new(py, &[]), None) {
            Err(e) => {
                assert!(py.get_type::<TypeError>() == e.get_type(py));
                // clear error from Python
                PyErr::fetch(py);
            }
            Ok(_) => assert!(false),
        }
    }
}
