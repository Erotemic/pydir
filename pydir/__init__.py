"""
mkinit pydir
"""
__version__ = '0.0.1.dev0'
from pydir import util_path
from pydir import util_platform

from pydir.util_path import (TempDir, augpath, compressuser, ensuredir,
                             truepath, userhome,)
from pydir.util_platform import (DARWIN, LINUX, POSIX, WIN32, editfile,
                                 ensure_app_cache_dir, ensure_app_resource_dir,
                                 get_app_cache_dir, get_app_resource_dir,
                                 platform_cache_dir, platform_resource_dir,
                                 startfile,)

__all__ = ['DARWIN', 'LINUX', 'POSIX', 'TempDir', 'WIN32', 'augpath',
           'compressuser', 'editfile', 'ensure_app_cache_dir',
           'ensure_app_resource_dir', 'ensuredir', 'get_app_cache_dir',
           'get_app_resource_dir', 'platform_cache_dir',
           'platform_resource_dir', 'startfile', 'truepath', 'userhome',
           'util_path', 'util_platform']
