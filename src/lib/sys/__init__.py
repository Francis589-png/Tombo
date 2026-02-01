"""
Tombo Sys Library - System Functions
"""
import sys
import platform

def tombo_version():
    """Get Python version."""
    return sys.version

def tombo_platform():
    """Get platform."""
    return sys.platform

def tombo_byteorder():
    """Get byte order."""
    return sys.byteorder

def tombo_maxsize():
    """Get max integer size."""
    return sys.maxsize

def tombo_argv():
    """Get command line arguments."""
    return sys.argv

def tombo_exit_code(code=0):
    """Exit with code."""
    sys.exit(int(code))

def tombo_stdin():
    """Get stdin."""
    return sys.stdin

def tombo_stdout():
    """Get stdout."""
    return sys.stdout

def tombo_stderr():
    """Get stderr."""
    return sys.stderr

def tombo_modules():
    """Get loaded modules."""
    return list(sys.modules.keys())

def tombo_path():
    """Get module search path."""
    return sys.path

def tombo_getsizeof(obj):
    """Get size of object in bytes."""
    return sys.getsizeof(obj)

def tombo_getrefcount(obj):
    """Get reference count of object."""
    return sys.getrefcount(obj)

def tombo_api_version():
    """Get Python API version."""
    return sys.api_version if hasattr(sys, 'api_version') else "Unknown"

def register(env):
    """Register sys library functions."""
    functions = {
        'version': tombo_version,
        'platform': tombo_platform,
        'byteorder': tombo_byteorder,
        'maxsize': tombo_maxsize,
        'argv': tombo_argv,
        'exit': tombo_exit_code,
        'stdin': tombo_stdin,
        'stdout': tombo_stdout,
        'stderr': tombo_stderr,
        'modules': tombo_modules,
        'path': tombo_path,
        'getsizeof': tombo_getsizeof,
        'getrefcount': tombo_getrefcount,
        'api_version': tombo_api_version,
    }
    for name, func in functions.items():
        env.set(name, func)
