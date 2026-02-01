"""
Tombo Core Library - Type Conversion, Object Operations, and Memory Management
"""

def tombo_int(value):
    """Convert value to integer."""
    if isinstance(value, bool):
        return 1 if value else 0
    elif isinstance(value, (int, float)):
        return int(value)
    elif isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            raise TypeError(f"Cannot convert string '{value}' to int")
    else:
        raise TypeError(f"Cannot convert {type(value).__name__} to int")

def tombo_float(value):
    """Convert value to float."""
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    elif isinstance(value, (int, float)):
        return float(value)
    elif isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            raise TypeError(f"Cannot convert string '{value}' to float")
    else:
        raise TypeError(f"Cannot convert {type(value).__name__} to float")

def tombo_str(value):
    """Convert value to string."""
    if isinstance(value, bool):
        return "true" if value else "false"
    elif value is None:
        return "null"
    elif isinstance(value, str):
        return value
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        items = ", ".join(tombo_str(v) for v in value)
        return f"[{items}]"
    elif isinstance(value, dict):
        items = ", ".join(f"{k}: {tombo_str(v)}" for k, v in value.items())
        return f"{{{items}}}"
    else:
        return str(value)

def tombo_bool(value):
    """Convert value to boolean."""
    if isinstance(value, bool):
        return value
    elif value is None:
        return False
    elif isinstance(value, (int, float)):
        return value != 0
    elif isinstance(value, str):
        return len(value) > 0
    elif isinstance(value, list):
        return len(value) > 0
    elif isinstance(value, dict):
        return len(value) > 0
    else:
        return bool(value)

def tombo_list(value):
    """Convert value to list."""
    if isinstance(value, list):
        return value
    elif isinstance(value, str):
        return list(value)
    elif isinstance(value, dict):
        return list(value.keys())
    else:
        return [value]

def tombo_dict(value=None):
    """Create or convert to dictionary."""
    if value is None:
        return {}
    elif isinstance(value, dict):
        return value
    elif isinstance(value, list):
        return {str(i): v for i, v in enumerate(value)}
    else:
        raise TypeError(f"Cannot convert {type(value).__name__} to dict")

def tombo_set(value=None):
    """Create or convert to set."""
    if value is None:
        return set()
    elif isinstance(value, set):
        return value
    elif isinstance(value, list):
        return set(value)
    elif isinstance(value, str):
        return set(value)
    else:
        raise TypeError(f"Cannot convert {type(value).__name__} to set")

def tombo_tuple(value=None):
    """Create or convert to tuple."""
    if value is None:
        return ()
    elif isinstance(value, tuple):
        return value
    elif isinstance(value, list):
        return tuple(value)
    elif isinstance(value, str):
        return tuple(value)
    else:
        return (value,)

def tombo_type(value):
    """Get the type of a value as a string."""
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, dict):
        return "dict"
    elif isinstance(value, set):
        return "set"
    elif isinstance(value, tuple):
        return "tuple"
    elif callable(value):
        return "function"
    else:
        return type(value).__name__

def tombo_isinstance(value, type_str):
    """Check if value is an instance of a type."""
    type_map = {
        "null": type(None),
        "bool": bool,
        "int": int,
        "float": float,
        "number": (int, float),
        "string": str,
        "list": list,
        "dict": dict,
        "set": set,
        "tuple": tuple,
        "function": callable,
    }
    
    if isinstance(type_str, str):
        type_class = type_map.get(type_str.lower())
        if type_class is None:
            raise ValueError(f"Unknown type: {type_str}")
        return isinstance(value, type_class)
    else:
        return isinstance(value, type_str)

def tombo_callable(value):
    """Check if value is callable."""
    return callable(value)

def tombo_id(value):
    """Get the identity (memory address) of a value."""
    return id(value)

def tombo_hash(value):
    """Get the hash of a value."""
    try:
        return hash(value)
    except TypeError:
        raise TypeError(f"Type {type(value).__name__} is not hashable")

def tombo_repr(value):
    """Get the detailed representation of a value."""
    return repr(value)

def tombo_dir(value):
    """Get list of attributes/methods of a value."""
    return [attr for attr in dir(value) if not attr.startswith('_')]

def tombo_getattr(obj, attr_name, default=None):
    """Get an attribute from an object."""
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        if default is not None:
            return default
        raise AttributeError(f"Object has no attribute '{attr_name}'")

def tombo_setattr(obj, attr_name, value):
    """Set an attribute on an object."""
    setattr(obj, attr_name, value)
    return value

def tombo_hasattr(obj, attr_name):
    """Check if an object has an attribute."""
    return hasattr(obj, attr_name)

def tombo_delattr(obj, attr_name):
    """Delete an attribute from an object."""
    delattr(obj, attr_name)
    return None

def tombo_copy(value):
    """Create a shallow copy of a value."""
    import copy
    return copy.copy(value)

def tombo_deep_copy(value):
    """Create a deep copy of a value."""
    import copy
    return copy.deepcopy(value)

def register(env):
    """Register core library functions in the interpreter environment."""
    builtins = {
        # Type conversion
        'int': tombo_int,
        'float': tombo_float,
        'str': tombo_str,
        'bool': tombo_bool,
        'list': tombo_list,
        'dict': tombo_dict,
        'set': tombo_set,
        'tuple': tombo_tuple,
        
        # Type checking
        'type': tombo_type,
        'isinstance': tombo_isinstance,
        'callable': tombo_callable,
        
        # Object operations
        'id': tombo_id,
        'hash': tombo_hash,
        'repr': tombo_repr,
        'dir': tombo_dir,
        'getattr': tombo_getattr,
        'setattr': tombo_setattr,
        'hasattr': tombo_hasattr,
        'delattr': tombo_delattr,
        
        # Copy operations
        'copy': tombo_copy,
        'deep_copy': tombo_deep_copy,
    }
    
    for name, func in builtins.items():
        env.set(name, func)
