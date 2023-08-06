r"""
Python interface to locate doxygen installation

If doxygen has been installed, this will use the doxygen binary
installed. Otherwise, it will download the latest release of
doxygen portable from http://doxygen.nl/files the first time
a function is called.
"""
import os
import shutil
import subprocess
from zipfile import ZipFile

__version__ = '1.2'
__author__ = 'Björn Rennfanz'
__license__ = 'MIT'

LATEST_RELEASE_URL = 'http://doxygen.nl/files/doxygen-1.8.20.windows.bin.zip'
DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), 'doxygen.exe')
INSTALL_X64_PATH = None
INSTALL_X86_PATH = None

if 'ProgramFiles(x86)' in os.environ:
    INSTALL_X86_PATH = os.path.join(os.environ['ProgramFiles(x86)'], 'doxygen', 'bin', 'doxygen.exe')

if 'ProgramFiles' in os.environ:
    INSTALL_X64_PATH = os.path.join(os.environ['ProgramFiles'], 'doxygen', 'bin', 'doxygen.exe')

alternate_path = None
download_mirror_url = None

def find(download=False, latest=False, prop=None, version=None):
    """
    Search doxygen installations and return an array of the results.
    If `latest` is true, returns only the newest version and last installed.
    If `download` is true, a portable doxygen version will downloaded.
    `prop` is the name of a property to return instead of the full installation details.
    `version` is a version range for instances to find. Example: '[1.0,2.0]' will find versions 1.*.
    """

    if download and not os.path.exists(DOWNLOAD_PATH):
        _download_doxygen_portable()

    def build_details_dict(path):
        """
        Helper to build doxygen details dictionary
        """
        result = {}
        result['installationVersion'] = subprocess.check_output([ path, '-v' ]).decode('utf-8').strip()
        result['installationPath'] = os.path.abspath(os.path.join(path, '..', '..')) if 'bin' in path else os.path.dirname(path)
        result['binaryPath'] = path

        return result

    # Try possible install locations
    results = []
    for doxygen_path in [ alternate_path, INSTALL_X64_PATH, INSTALL_X86_PATH, DOWNLOAD_PATH ]:
        if doxygen_path and os.path.exists(doxygen_path):
            results.append(build_details_dict(doxygen_path))

    def get_version(value):
        """
        Helper to extract version from details dictionary
        """
        return value['installationVersion']

    if version:
        # Convert string to array and filter versions
        version_range = version.replace('[', '').replace(']', '').split(',')
        results = list(filter(lambda x: get_version(x) > str(version_range[0]) and get_version(x) < str(version_range[1]), results))

    if results and latest:
        # Sort asscending version and get hightest
        results.sort(key = get_version, reverse = True)
        results = [ results[0] ]

    # Filter results using wanted property
    if results and prop:
        filter_results = []
        for result in results:
            filter_results.append( { key:value for (key, value) in result.items() if prop in key }[prop] )

        return filter_results

    return results

def find_first(**kwargs):
    """
    Search doxygen and return the first result, or None if there are no results.

    See find() for parameters.
    """
    return next(iter(find(**kwargs)), None)

def get_latest():
    """
    Get the information for the latest installed version of doxygen.
    Returns None if no installations could be found.
    """
    return find_first(download=True, latest=True)

def get_latest_path():
    """
    Get the file path to the latest installed version of doxygen.
    Returns None if no installations could be found.
    """
    return find_first(download=True, latest=True, prop='installationPath')

def get_latest_version():
    """
    Get the version string of the latest installed version of doxygen.
    Returns None if no installations could be found.
    """
    return find_first(download=True, latest=True, prop='installationVersion')

def get_doxygen_path():
    """
    Get the path to doxygen.exe.
    If doxygen is not already installed, and no alternate path
    is given using `set_doxygen_path()`, the latest release will
    be downloaded and stored alongside this script.
    """
    return find_first(download=True, latest=True, prop='binaryPath')

def set_doxygen_path(path):
    """
    Set the path to doxygen.exe.
    If this is set, it overrides any version installed.
    """
    global alternate_path
    alternate_path = path

def set_download_mirror(url):
    """
    Set a URL from which doxygen portable should be downloaded if it is not already
    installed and no alternate path is given using `set_doxygen_path()`.
    """
    global download_mirror_url
    download_mirror_url = url

def _download_doxygen_portable():
    """
    Download doxygen portable to DOWNLOAD_PATH.
    """
    print('Downloading from', _get_latest_release_url())
    download_zip_path = os.path.join(os.path.dirname(DOWNLOAD_PATH), 'doxygen.zip')
    try:
        from urllib.request import urlopen
        with urlopen(_get_latest_release_url()) as response, open(download_zip_path, 'wb') as outfile:
            shutil.copyfileobj(response, outfile)
    except ImportError:
        # Python 2
        import urllib
        urllib.urlretrieve(_get_latest_release_url(), download_zip_path)

    with ZipFile(download_zip_path, 'r') as zipFile:
        zipFile.extractall(path=os.path.dirname(download_zip_path))

def _get_latest_release_url():
    """
    The the URL of the latest release of doxygen portable.
    """
    if download_mirror_url:
        return download_mirror_url

    return LATEST_RELEASE_URL
