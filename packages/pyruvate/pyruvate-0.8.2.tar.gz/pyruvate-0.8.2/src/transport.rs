use libsystemd::activation::{receive_descriptors, IsType};
use mio::event::Source;
use mio::net::{TcpListener, TcpStream, UnixListener, UnixStream};
use nix::fcntl::{fcntl, FcntlArg, OFlag};
use std::error;
use std::fmt::Debug;
use std::io;
use std::net;
use std::os::unix::io::{AsRawFd, FromRawFd, IntoRawFd, RawFd};

pub type Result<T> = std::result::Result<T, Box<dyn error::Error>>;

// we need AsRawFd for sendfile
pub trait Write: io::Write + AsRawFd {}
impl<T: io::Write + AsRawFd> Write for T {}

pub trait NonBlockingWrite: Write + Send + Source {}
impl<T: Write + Send + Source> NonBlockingWrite for T {}

pub trait BlockingWrite: Socket + SetBlocking {}
impl<T: Socket + SetBlocking> BlockingWrite for T {}

pub trait Read: io::Read {
    fn peer_addr(&self) -> String;
}

impl Read for TcpStream {
    fn peer_addr(&self) -> String {
        match TcpStream::peer_addr(&self) {
            Ok(addr) => format!("{}", addr.ip()),
            Err(_) => String::new(),
        }
    }
}

impl Read for UnixStream {
    fn peer_addr(&self) -> String {
        match UnixStream::peer_addr(&self) {
            Ok(addr) => {
                if let Some(addr) = addr.as_pathname() {
                    match addr.as_os_str().to_os_string().into_string() {
                        Ok(addr) => addr,
                        Err(_) => String::new(),
                    }
                } else {
                    String::new()
                }
            }
            Err(_) => String::new(),
        }
    }
}

pub fn would_block(err: &io::Error) -> bool {
    err.kind() == io::ErrorKind::WouldBlock
}

/// set a file descriptor into blocking mode
pub trait SetBlocking: AsRawFd {
    fn set_blocking(&mut self) -> Result<()>;
}

impl<T: AsRawFd> SetBlocking for T {
    #[inline]
    fn set_blocking(&mut self) -> Result<()> {
        let flags = fcntl(self.as_raw_fd(), FcntlArg::F_GETFL)?;
        let mut new_flags = OFlag::from_bits(flags).expect("Could not create flags from bits");
        new_flags.remove(OFlag::O_NONBLOCK);
        fcntl(self.as_raw_fd(), FcntlArg::F_SETFL(new_flags))?;
        Ok(())
    }
}

/// set a file descriptor into non-blocking mode
pub trait SetNonBlocking {
    type Fd;
    fn set_nonblocking(self) -> Result<Self::Fd>;
}

impl SetNonBlocking for RawFd {
    type Fd = RawFd;
    #[inline]
    fn set_nonblocking(self) -> Result<Self::Fd> {
        let flags = fcntl(self, FcntlArg::F_GETFL)?;
        let mut new_flags = OFlag::from_bits(flags).expect("Could not create flags from bits");
        new_flags.insert(OFlag::O_NONBLOCK);
        fcntl(self, FcntlArg::F_SETFL(new_flags))?;
        Ok(self)
    }
}

pub trait Socket: AsRawFd + io::Write + Read + Send + Source {}

impl<S: AsRawFd + io::Write + Read + Send + Source> Socket for S {}

/// commonalities of TCPListener + UnixListener
pub trait Listening {
    type Connected: Socket + Debug + SetBlocking;
    fn accept(&self) -> io::Result<Self::Connected>;
    fn local_addr_string(&self) -> String;
}

// s. https://stackoverflow.com/questions/53713354/implementing-traits-without-repeating-methods-already-defined-on-the-struct
impl Listening for TcpListener {
    type Connected = TcpStream;
    fn accept(&self) -> io::Result<Self::Connected> {
        match TcpListener::accept(&self) {
            Ok((conn, _)) => Ok(conn),
            Err(e) => Err(e),
        }
    }

    fn local_addr_string(&self) -> String {
        match self.local_addr() {
            Ok(addr) => format!("{}", addr),
            Err(e) => format!("TCPListener error: {:?}", e),
        }
    }
}

impl Listening for UnixListener {
    type Connected = UnixStream;
    fn accept(&self) -> io::Result<Self::Connected> {
        match UnixListener::accept(&self) {
            Ok((conn, _)) => Ok(conn),
            Err(e) => Err(e),
        }
    }

    fn local_addr_string(&self) -> String {
        match self.local_addr() {
            Ok(addr) => match addr.as_pathname() {
                Some(path) => format!("{}", path.display()),
                None => " - ".to_string(),
            },
            Err(e) => format!("UnixListener error: {:?}", e),
        }
    }
}

pub trait Listener: Listening + Source + FromRawFd {}
impl<L: Listening + Source + FromRawFd> Listener for L {}

pub trait SocketActivation: Sized + FromRawFd {
    /// get a socket activated by systemd
    fn from_active_socket() -> Result<Self>;
}

macro_rules! create_from_active_socket {
    ($S: ty, $testfn: ident, $errmsg: literal) => {
        match receive_descriptors(false) {
            Ok(mut possible_fds) => {
                // check whether systemd has passed a valid file descriptor
                if !possible_fds.is_empty() {
                    let fd = possible_fds.remove(0);
                    if fd.$testfn() {
                        let rawfd = fd.into_raw_fd().set_nonblocking()?;
                        Ok(unsafe { <$S>::from_raw_fd(rawfd) })
                    } else {
                        Err(Box::new(io::Error::new(io::ErrorKind::Other, $errmsg)))
                    }
                } else {
                    Err(Box::new(io::Error::new(
                        io::ErrorKind::Other,
                        "Could not get file descriptors",
                    )))
                }
            }
            Err(e) => Err(Box::new(e)),
        }
    };
}

impl SocketActivation for TcpListener {
    fn from_active_socket() -> Result<TcpListener> {
        create_from_active_socket!(TcpListener, is_inet, "File descriptor must be a TCP socket")
    }
}

impl SocketActivation for UnixListener {
    fn from_active_socket() -> Result<UnixListener> {
        create_from_active_socket!(
            UnixListener,
            is_unix,
            "File descriptor must be a Unix Domain socket"
        )
    }
}

pub fn parse_server_info(addr: &str) -> (String, String) {
    match addr.parse::<net::SocketAddr>() {
        Ok(ipaddr) => (format!("{}", ipaddr.ip()), format!("{}", ipaddr.port())),
        Err(_) => (String::from(addr), String::new()),
    }
}

#[cfg(test)]
mod tests {

    use log::debug;
    use mio::net::{self, TcpListener, UnixListener, UnixStream};
    use nix::fcntl::{fcntl, FcntlArg, OFlag};
    use nix::unistd::dup2;
    use std::env::set_var;
    use std::fs::remove_file;
    use std::io;
    use std::net::SocketAddr;
    use std::os::unix::io::AsRawFd;
    use std::process::id;
    use std::sync::mpsc::channel;
    use std::thread;
    use tempfile::tempfile;

    use crate::transport::{
        parse_server_info, would_block, Listening, Read, SetNonBlocking, SocketActivation,
    };

    #[test]
    fn test_would_block() {
        let wbe = io::Error::new(io::ErrorKind::WouldBlock, "foo");
        assert!(would_block(&wbe));
        let nwbe = io::Error::new(io::ErrorKind::Other, "foo");
        assert!(!would_block(&nwbe));
    }

    #[test]
    fn test_set_nonblocking() {
        let addr: SocketAddr = "127.0.0.1:0".parse().unwrap();
        let listener = TcpListener::bind(addr).unwrap();
        let before = net::TcpStream::connect(listener.local_addr().unwrap()).unwrap();
        let o_before =
            OFlag::from_bits(fcntl(before.as_raw_fd(), FcntlArg::F_GETFL).unwrap()).unwrap();
        assert!(o_before.contains(OFlag::O_NONBLOCK));
        match before.as_raw_fd().set_nonblocking() {
            Ok(after) => {
                let o_after = OFlag::from_bits(fcntl(after, FcntlArg::F_GETFL).unwrap()).unwrap();
                assert!(o_after.contains(OFlag::O_NONBLOCK));
            }
            Err(_) => {
                assert!(false);
            }
        }
    }

    #[test]
    fn test_from_active_socket_tcp() {
        // no systemd environment
        match TcpListener::from_active_socket() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // no file descriptors
        set_var("LISTEN_FDS", "0");
        set_var("LISTEN_PID", format!("{}", id()));
        match TcpListener::from_active_socket() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // file descriptor is not a socket
        let tmp = tempfile().unwrap();
        dup2(tmp.as_raw_fd(), 3).unwrap();
        set_var("LISTEN_FDS", "1");
        set_var("LISTEN_PID", format!("{}", id()));
        match TcpListener::from_active_socket() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // Success
        let si = "127.0.0.1:0".parse().unwrap();
        let listener = TcpListener::bind(si).unwrap();
        dup2(listener.as_raw_fd(), 3).unwrap(); // must be >= 3 (SD_LISTEN_FDS_START)
                                                // see libsystemd.activation for how this works
        set_var("LISTEN_FDS", "1");
        set_var("LISTEN_PID", format!("{}", id()));
        match TcpListener::from_active_socket() {
            Ok(sock) => {
                assert!(sock.as_raw_fd() == 3);
            }
            Err(_) => assert!(false),
        }
    }

    #[test]
    fn test_from_active_socket_unix() {
        // no file descriptors
        set_var("LISTEN_FDS", "0");
        set_var("LISTEN_PID", format!("{}", id()));
        match UnixListener::from_active_socket() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // file descriptor is not a socket
        let si = "127.0.0.1:0".parse().unwrap();
        let tcp = TcpListener::bind(si).unwrap();
        dup2(tcp.as_raw_fd(), 3).unwrap();
        set_var("LISTEN_FDS", "1");
        set_var("LISTEN_PID", format!("{}", id()));
        match UnixListener::from_active_socket() {
            Ok(_) => assert!(false),
            Err(e) => debug!("Error: {:?}", e),
        }
        // Success
        let si = "/tmp/test.socket";
        let listener = UnixListener::bind(si).unwrap();
        dup2(listener.as_raw_fd(), 3).unwrap(); // must be >= 3 (SD_LISTEN_FDS_START)
                                                // see libsystemd.activation for how this works
        set_var("LISTEN_FDS", "1");
        set_var("LISTEN_PID", format!("{}", id()));
        match UnixListener::from_active_socket() {
            Ok(sock) => {
                debug!("{:?}", sock);
                assert!(sock.as_raw_fd() == 3);
            }
            Err(e) => {
                debug!("Error: {:?}", e);
                assert!(false)
            }
        }
        remove_file("/tmp/test.socket").unwrap();
    }

    #[test]
    fn test_parse_server_info() {
        assert!(
            parse_server_info("127.0.0.1:7878") == ("127.0.0.1".to_string(), "7878".to_string())
        );
        assert!(
            parse_server_info("/tmp/pyruvate.sock")
                == ("/tmp/pyruvate.sock".to_string(), String::new())
        );
    }

    #[test]
    fn test_local_addr_string_tcp() {
        let si = "127.0.0.1:33333".parse().unwrap();
        let listener = TcpListener::bind(si).unwrap();
        assert!(listener.local_addr_string() == "127.0.0.1:33333");
    }

    #[test]
    fn test_local_addr_string_unix() {
        let si = "/tmp/test.socket";
        let listener = UnixListener::bind(si).unwrap();
        assert!(listener.local_addr_string() == "/tmp/test.socket");
        remove_file("/tmp/test.socket").unwrap();
    }

    #[test]
    fn test_peer_addr_unix() {
        let si = "/tmp/test.socket";
        let _listener = UnixListener::bind(si).unwrap();
        let socket = UnixStream::connect(si).unwrap();
        let got = Read::peer_addr(&socket);
        remove_file("/tmp/test.socket").unwrap();
        assert_eq!(got, "/tmp/test.socket");
    }

    #[test]
    fn test_listening_unix_accept() {
        let si = "/tmp/foo.socket";
        let server = UnixListener::bind(si).unwrap();
        let (tx, rx) = channel();
        let (snd, got) = channel();
        thread::spawn(move || {
            match Listening::accept(&server) {
                Ok(conn) => {
                    snd.clone().send(conn).unwrap();
                }
                Err(_) => {
                    assert!(false);
                }
            }
            rx.recv().unwrap();
        });
        let _socket = UnixStream::connect(si).unwrap();
        let conn = got.recv().unwrap();
        assert_eq!(
            conn.local_addr()
                .unwrap()
                .as_pathname()
                .unwrap()
                .as_os_str(),
            "/tmp/foo.socket"
        );
        tx.send(()).unwrap();
        remove_file("/tmp/foo.socket").unwrap();
    }

    #[test]
    fn test_listening_unix_local_addr_string() {
        let si = "/tmp/foo.socket";
        let server = UnixListener::bind(si).unwrap();
        let got = server.local_addr_string();
        remove_file("/tmp/foo.socket").unwrap();
        assert_eq!(got, "/tmp/foo.socket");
    }
}
