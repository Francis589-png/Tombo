"""
Tombo OS Library - Operating System Functions
"""
import os
import platform
import subprocess

def tombo_getenv(name, default=''):
    """Get environment variable."""
    return os.getenv(str(name), str(default))

def tombo_setenv(name, value):
    """Set environment variable."""
    os.environ[str(name)] = str(value)
    return None

def tombo_environ():
    """Get all environment variables as dict."""
    return dict(os.environ)

def tombo_platform():
    """Get platform name."""
    return platform.system()

def tombo_arch():
    """Get architecture."""
    return platform.machine()

def tombo_cpu_count():
    """Get number of CPUs."""
    return os.cpu_count()

def tombo_hostname():
    """Get hostname."""
    return platform.node()

def tombo_username():
    """Get username."""
    try:
        return os.getlogin()
    except:
        return os.environ.get('USER', os.environ.get('USERNAME', 'unknown'))

def tombo_exec(command):
    """Execute command."""
    try:
        result = subprocess.run(str(command), shell=True, capture_output=True, text=True)
        return {'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
    except Exception as e:
        raise RuntimeError(f"Cannot execute command: {e}")

def tombo_pid():
    """Get process ID."""
    return os.getpid()

def tombo_exit(code=0):
    """Exit program."""
    import sys
    sys.exit(int(code))

def tombo_sep():
    """Get path separator."""
    return os.sep

def tombo_linesep():
    """Get line separator."""
    return os.linesep

def tombo_devnull():
    """Get dev/null path."""
    return os.devnull

def register(env):
    """Register OS library functions."""
    functions = {
        'getenv': tombo_getenv,
        'setenv': tombo_setenv,
        'environ': tombo_environ,
        'platform': tombo_platform,
        'arch': tombo_arch,
        'cpu_count': tombo_cpu_count,
        'hostname': tombo_hostname,
        'username': tombo_username,
        'exec': tombo_exec,
        'pid': tombo_pid,
        'exit': tombo_exit,
        'sep': tombo_sep,
        'linesep': tombo_linesep,
        'devnull': tombo_devnull,
    }
    for name, func in functions.items():
        env.set(name, func)
