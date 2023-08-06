# Python doxygenwhere

This module searches for doxygen installations on system.

# Usage
`find` and `find_first` are the most generic functions.
`find` returns a list of installed doxygen matching the
given options, and `find_first` returns only the first result.

If you are only interested in the latest version of doxygen, use
`get_latest`. To get just the installation path, use `get_latest_path`. To get
just the version number, use `get_latest_version`.

If you want to use your own version of doxygen.exe instead of the one installed
on your system, use `set_doxygen_path` to provide its location.

If you want to use a mirror instead of offical doxygen webserver to download
portable doxygen, for example when on an intranet that does not have access
to Internet, use `set_download_mirror` and provide the URL of the mirror.
