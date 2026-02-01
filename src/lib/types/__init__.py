"""
Tombo Types Library - Type Operations
"""

def tombo_typeof(value):
    """Get type of value."""
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return 'bool'
    elif isinstance(value, int):
        return 'int'
    elif isinstance(value, float):
        return 'float'
    elif isinstance(value, str):
        return 'string'
    elif isinstance(value, list):
        return 'list'
    elif isinstance(value, dict):
        return 'dict'
    elif isinstance(value, set):
        return 'set'
    elif isinstance(value, tuple):
        return 'tuple'
    elif callable(value):
        return 'function'
    else:
        return type(value).__name__

def tombo_instance_of(value, type_name):
    """Check instance of type."""
    type_map = {
        'null': type(None),
        'bool': bool,
        'int': int,
        'float': float,
        'number': (int, float),
        'string': str,
        'list': list,
        'dict': dict,
        'set': set,
        'tuple': tuple,
        'function': callable,
    }
    type_class = type_map.get(str(type_name).lower())
    return isinstance(value, type_class) if type_class else False

def tombo_is_number(value):
    """Check if number."""
    return isinstance(value, (int, float))

def tombo_is_string(value):
    """Check if string."""
    return isinstance(value, str)

def tombo_is_list(value):
    """Check if list."""
    return isinstance(value, list)

def tombo_is_dict(value):
    """Check if dict."""
    return isinstance(value, dict)

def tombo_is_set(value):
    """Check if set."""
    return isinstance(value, set)

def tombo_is_tuple(value):
    """Check if tuple."""
    return isinstance(value, tuple)

def tombo_is_none(value):
    """Check if None."""
    return value is None

def tombo_is_callable(value):
    """Check if callable."""
    return callable(value)

def tombo_is_function(value):
    """Check if function."""
    return callable(value)

def tombo_is_class(value):
    """Check if class."""
    return isinstance(value, type)

def tombo_subtype_of(value, parent_type):
    """Check if subtype."""
    try:
        return issubclass(type(value), parent_type)
    except:
        return False

def tombo_convertible_to(value, target_type):
    """Check if convertible to type."""
    target = str(target_type).lower()
    try:
        if target == 'int':
            int(value)
            return True
        elif target == 'float':
            float(value)
            return True
        elif target == 'string':
            str(value)
            return True
        elif target == 'bool':
            bool(value)
            return True
        elif target == 'list':
            list(value) if hasattr(value, '__iter__') else False
            return True
    except:
        return False
    return False

def tombo_type_name(value):
    """Get type name as string."""
    return tombo_typeof(value)

def register(env):
    """Register types library functions."""
    functions = {
        'typeof': tombo_typeof,
        'instance_of': tombo_instance_of,
        'is_number': tombo_is_number,
        'is_string': tombo_is_string,
        'is_list': tombo_is_list,
        'is_dict': tombo_is_dict,
        'is_set': tombo_is_set,
        'is_tuple': tombo_is_tuple,
        'is_none': tombo_is_none,
        'is_callable': tombo_is_callable,
        'is_function': tombo_is_function,
        'is_class': tombo_is_class,
        'subtype_of': tombo_subtype_of,
        'convertible_to': tombo_convertible_to,
        'type_name': tombo_type_name,
    }
    for name, func in functions.items():
        env.set(name, func)
