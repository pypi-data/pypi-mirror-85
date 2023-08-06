Changelog
=========

0.8.2 (2020-11-17)
------------------

* Fix blocksize handling for sendfile case
* Format unix stream peer address
* Use latest mio

0.8.1 (2020-11-10)
------------------

* Receiver in non-blocking worker must not block when channel is empty

0.8.0 (2020-11-07)
------------------

* Logging overhaul
* New async_logging option
* Some performance improvements
* Support Python 3.9
* Switch to manylinux2010 platform tag

0.7.1 (2020-09-16)
------------------

* Raise Python exception when socket is unavailable
* Add Pyramid configuration example in readme

0.7.0 (2020-08-30)
------------------

* Use Python logging
* Display server info on startup
* Fix socket activation for unix domain sockets

0.6.2 (2020-08-12)
------------------

* Improved logging
* PasteDeploy entry point now also uses at most 24 headers by default

0.6.1 (2020-08-10)
------------------

* Improve request parsing
* Increase default maximum number of headers to 24

0.6.0 (2020-07-29)
------------------

* Support unix domain sockets
* Improve sendfile usage

0.5.3 (2020-07-15)
------------------

* Fix testing for completed sendfile call in case of EAGAIN

0.5.2 (2020-07-15)
------------------

* Fix testing for completed response in case of EAGAIN
* Cargo update

0.5.1 (2020-07-07)
------------------

* Fix handling of read events
* Fix changelog
* Cargo update
* 'Interrupted' error is not a todo
* Remove unused code

0.5.0 (2020-06-07)
------------------

* Add support for systemd socket activation

0.4.0 (2020-06-29)
------------------

* Add a new worker that does nonblocking write
* Add default arguments
* Add option to configure maximum number of request headers
* Add Via header

0.3.0 (2020-06-16)
------------------

* Switch to rust-cpython
* Fix passing of tcp connections to worker threads

0.2.0 (2020-03-10)
------------------

* Added some Python tests (using py.test and tox)
* Improve handling of HTTP headers
* Respect content length header when using sendfile

0.1.0 (2020-02-10)
------------------

* Initial release
