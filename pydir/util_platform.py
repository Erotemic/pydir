# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from os.path import exists
from os.path import expanduser
from os.path import join
from os.path import normpath
import os
import sys
import pipes
import six
from pydir import util_path

WIN32  = sys.platform.startswith('win32')
LINUX  = sys.platform.startswith('linux')
DARWIN = sys.platform.startswith('darwin')
POSIX = 'posix' in sys.builtin_module_names


def platform_resource_dir():  # nocover
    """
    Returns a directory which should be writable for any application
    This should be used for persistent configuration files.

    Returns:
        str : path to the resource dir used by the current operating system
    """
    if WIN32:
        dpath_ = '~/AppData/Roaming'
    elif LINUX:
        dpath_ = '~/.config'
    elif DARWIN:
        dpath_  = '~/Library/Application Support'
    else:
        raise NotImplementedError('Unknown Platform  %r' % (sys.platform,))
    dpath = normpath(expanduser(dpath_))
    return dpath


def platform_cache_dir():  # nocover
    """
    Returns a directory which should be writable for any application
    This should be used for temporary deletable data.

    Returns:
        str : path to the cache dir used by the current operating system
    """
    if WIN32:
        dpath_ = '~/AppData/Local'
    elif LINUX:
        dpath_ = '~/.cache'
    elif DARWIN:
        dpath_  = '~/Library/Caches'
    else:
        raise NotImplementedError('Unknown Platform  %r' % (sys.platform,))
    dpath = normpath(expanduser(dpath_))
    return dpath


def startfile(fpath, verbose=True):  # nocover
    """
    Uses default program defined by the system to open a file.
    This is done via `os.startfile` on windows, `open` on mac, and `xdg-open`
    on linux.

    Args:
        fpath (str): a file to open using the program associated with the
            files extension type.
        verbose (int): verbosity

    References:
        http://stackoverflow.com/questions/2692873/quote-posix

    DisableExample:
        >>> # This test interacts with a GUI frontend, not sure how to test.
        >>> import pydir as pydir
        >>> base = pydir.ensure_app_cache_dir('pydir')
        >>> fpath1 = join(base, 'test_open.txt')
        >>> pydir.touch(fpath1)
        >>> proc = pydir.startfile(fpath1)
    """
    from pydir import util_cmd
    if verbose:
        print('[pydir] startfile("{}")'.format(fpath))
    fpath = normpath(fpath)
    if not exists(fpath):
        raise Exception('Cannot start nonexistant file: %r' % fpath)
    if not WIN32:
        fpath = pipes.quote(fpath)
    if LINUX:
        info = util_cmd.cmd(('xdg-open', fpath), detatch=True, verbose=verbose)
    elif DARWIN:
        info = util_cmd.cmd(('open', fpath), detatch=True, verbose=verbose)
    elif WIN32:
        os.startfile(fpath)
        info = None
    else:
        raise RuntimeError('Unknown Platform')
    if info is not None:
        if not info['proc']:
            raise Exception('startfile failed')


def editfile(fpath, verbose=True):  # nocover
    """
    Opens a file or code corresponding to a live python object in your
    preferred visual editor. This function is mainly useful in an interactive
    IPython session.

    The visual editor is determined by the `VISUAL` environment variable.  If
    this is not specified it defaults to gvim.

    Args:
        fpath (str): a file path or python module / function
        verbose (int): verbosity

    DisableExample:
        >>> # This test interacts with a GUI frontend, not sure how to test.
        >>> import pydir
        >>> pydir.editfile(pydir.util_platform.__file__)
        >>> pydir.editfile(pydir)
        >>> pydir.editfile(pydir.editfile)
    """
    from six import types
    from pydir import util_cmd
    if not isinstance(fpath, six.string_types):
        if isinstance(fpath, types.ModuleType):
            fpath = fpath.__file__
        else:
            fpath =  sys.modules[fpath.__module__].__file__
        fpath_py = fpath.replace('.pyc', '.py')
        if exists(fpath_py):
            fpath = fpath_py

    if verbose:
        print('[pydir] editfile("{}")'.format(fpath))

    editor = os.environ.get('VISUAL', 'gvim')

    if not exists(fpath):
        raise IOError('Cannot start nonexistant file: %r' % fpath)
    util_cmd.cmd([editor, fpath], fpath, detatch=True)


def get_app_resource_dir(appname, *args):
    """
    Returns a writable directory for an application
    This should be used for persistent configuration files.

    Args:
        appname (str): the name of the application
        *args: any other subdirectories may be specified

    Returns:
        str: dpath: writable resource directory for this application

    SeeAlso:
        ensure_app_resource_dir
    """
    dpath = join(platform_resource_dir(), appname, *args)
    return dpath


def ensure_app_resource_dir(appname, *args):
    """
    Calls `get_app_resource_dir` but ensures the directory exists.

    SeeAlso:
        get_app_resource_dir

    Example:
        >>> import pydir as pydir
        >>> dpath = pydir.ensure_app_resource_dir('pydir')
        >>> assert exists(dpath)
    """
    dpath = get_app_resource_dir(appname, *args)
    util_path.ensuredir(dpath)
    return dpath


def get_app_cache_dir(appname, *args):
    """
    Returns a writable directory for an application.
    This should be used for temporary deletable data.

    Args:
        appname (str): the name of the application
        *args: any other subdirectories may be specified

    Returns:
        str: dpath: writable cache directory for this application

    SeeAlso:
        ensure_app_cache_dir
    """
    dpath = join(platform_cache_dir(), appname, *args)
    return dpath


def ensure_app_cache_dir(appname, *args):
    """
    Calls `get_app_cache_dir` but ensures the directory exists.

    SeeAlso:
        get_app_cache_dir

    Example:
        >>> import pydir as pydir
        >>> dpath = pydir.ensure_app_cache_dir('pydir')
        >>> assert exists(dpath)
    """
    dpath = get_app_cache_dir(appname, *args)
    util_path.ensuredir(dpath)
    return dpath


if __name__ == '__main__':
    """
    CommandLine:
        python -m pydir.util_platform
        python -m pydir.util_platform all
        pytest pydir/util_platform.py
    """
    import xdoctest as xdoc
    xdoc.doctest_module()
