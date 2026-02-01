"""
Tombo I/O Library - Input/Output and File Operations
"""
import os
import os.path

# Console I/O (print already in core, adding companions)
def tombo_println(value=''):
    """Print with newline."""
    print(value)
    return None

def tombo_input(prompt=''):
    """Read string input."""
    return input(str(prompt))

def tombo_ask(prompt=''):
    """Alias for input() - ask user for input."""
    return input(str(prompt))

def tombo_input_number(prompt=''):
    """Read numeric input."""
    try:
        return float(input(str(prompt)))
    except ValueError:
        raise ValueError("Input must be a number")

def tombo_input_bool(prompt=''):
    """Read boolean input."""
    response = input(str(prompt)).lower()
    return response in ('true', 't', 'yes', 'y', '1')

def tombo_eprint(value=''):
    """Print to stderr."""
    import sys
    print(value, file=sys.stderr)
    return None

def tombo_eprintln(value=''):
    """Print to stderr with newline."""
    import sys
    print(value, file=sys.stderr)
    return None

# File I/O
def tombo_read_file(path):
    """Read entire file as string."""
    try:
        with open(str(path), 'r', encoding='utf-8') as f:
            return f.read()
    except IOError as e:
        raise IOError(f"Cannot read file '{path}': {e}")

def tombo_write_file(path, content):
    """Write content to file (overwrites)."""
    try:
        with open(str(path), 'w', encoding='utf-8') as f:
            f.write(str(content))
        return True
    except IOError as e:
        raise IOError(f"Cannot write file '{path}': {e}")

def tombo_append_file(path, content):
    """Append content to file."""
    try:
        with open(str(path), 'a', encoding='utf-8') as f:
            f.write(str(content))
        return True
    except IOError as e:
        raise IOError(f"Cannot append to file '{path}': {e}")

def tombo_file_exists(path):
    """Check if file exists."""
    return os.path.isfile(str(path))

def tombo_is_file(path):
    """Check if path is a file."""
    return os.path.isfile(str(path))

def tombo_is_dir(path):
    """Check if path is a directory."""
    return os.path.isdir(str(path))

def tombo_delete_file(path):
    """Delete a file."""
    try:
        os.remove(str(path))
        return True
    except OSError as e:
        raise OSError(f"Cannot delete file '{path}': {e}")

def tombo_copy_file(src, dst):
    """Copy file."""
    try:
        import shutil
        shutil.copy2(str(src), str(dst))
        return True
    except OSError as e:
        raise OSError(f"Cannot copy file: {e}")

def tombo_move_file(src, dst):
    """Move/rename file."""
    try:
        import shutil
        shutil.move(str(src), str(dst))
        return True
    except OSError as e:
        raise OSError(f"Cannot move file: {e}")

def tombo_rename_file(src, dst):
    """Rename file (alias for move)."""
    return tombo_move_file(src, dst)

def tombo_file_size(path):
    """Get file size in bytes."""
    try:
        return os.path.getsize(str(path))
    except OSError as e:
        raise OSError(f"Cannot get file size: {e}")

def tombo_file_time(path):
    """Get file modification time."""
    try:
        return os.path.getmtime(str(path))
    except OSError as e:
        raise OSError(f"Cannot get file time: {e}")

# Directory operations
def tombo_list_dir(path='.'):
    """List directory contents."""
    try:
        return os.listdir(str(path))
    except OSError as e:
        raise OSError(f"Cannot list directory: {e}")

def tombo_make_dir(path, parents=False):
    """Create directory."""
    try:
        if parents:
            os.makedirs(str(path), exist_ok=True)
        else:
            os.mkdir(str(path))
        return True
    except OSError as e:
        raise OSError(f"Cannot create directory: {e}")

def tombo_remove_dir(path):
    """Remove directory."""
    try:
        os.rmdir(str(path))
        return True
    except OSError as e:
        raise OSError(f"Cannot remove directory: {e}")

def tombo_change_dir(path):
    """Change current directory."""
    try:
        os.chdir(str(path))
        return True
    except OSError as e:
        raise OSError(f"Cannot change directory: {e}")

def tombo_current_dir():
    """Get current directory."""
    return os.getcwd()

def tombo_walk_dir(path):
    """Walk directory tree."""
    result = []
    try:
        for root, dirs, files in os.walk(str(path)):
            result.append({
                'path': root,
                'dirs': dirs,
                'files': files
            })
    except OSError as e:
        raise OSError(f"Cannot walk directory: {e}")
    return result

def tombo_glob(pattern):
    """Find files matching pattern."""
    import glob
    return glob.glob(str(pattern))

# Path operations
def tombo_path_join(*parts):
    """Join path components."""
    return os.path.join(*[str(p) for p in parts])

def tombo_path_split(path):
    """Split path into directory and filename."""
    result = os.path.split(str(path))
    return list(result)

def tombo_path_base(path):
    """Get basename."""
    return os.path.basename(str(path))

def tombo_path_dir(path):
    """Get directory part."""
    return os.path.dirname(str(path))

def tombo_path_ext(path):
    """Get file extension."""
    return os.path.splitext(str(path))[1]

def tombo_path_abs(path):
    """Get absolute path."""
    return os.path.abspath(str(path))

def tombo_path_rel(path, start='.'):
    """Get relative path."""
    return os.path.relpath(str(path), str(start))

def tombo_path_norm(path):
    """Normalize path."""
    return os.path.normpath(str(path))

def register(env):
    """Register I/O library functions in the interpreter environment."""
    functions = {
        # Console I/O
        'println': tombo_println,
        'input': tombo_input,
        'ask': tombo_ask,
        'input_number': tombo_input_number,
        'input_bool': tombo_input_bool,
        'eprint': tombo_eprint,
        'eprintln': tombo_eprintln,
        
        # File I/O
        'read_file': tombo_read_file,
        'write_file': tombo_write_file,
        'append_file': tombo_append_file,
        'file_exists': tombo_file_exists,
        'is_file': tombo_is_file,
        'is_dir': tombo_is_dir,
        'delete_file': tombo_delete_file,
        'copy_file': tombo_copy_file,
        'move_file': tombo_move_file,
        'rename_file': tombo_rename_file,
        'file_size': tombo_file_size,
        'file_time': tombo_file_time,
        
        # Directory operations
        'list_dir': tombo_list_dir,
        'make_dir': tombo_make_dir,
        'remove_dir': tombo_remove_dir,
        'change_dir': tombo_change_dir,
        'current_dir': tombo_current_dir,
        'walk_dir': tombo_walk_dir,
        'glob': tombo_glob,
        
        # Path operations
        'path_join': tombo_path_join,
        'path_split': tombo_path_split,
        'path_base': tombo_path_base,
        'path_dir': tombo_path_dir,
        'path_ext': tombo_path_ext,
        'path_abs': tombo_path_abs,
        'path_rel': tombo_path_rel,
        'path_norm': tombo_path_norm,
    }
    
    for name, func in functions.items():
        env.set(name, func)
