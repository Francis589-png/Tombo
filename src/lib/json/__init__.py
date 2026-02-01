"""
Tombo JSON Library - JSON Processing
"""
import json

def tombo_stringify(obj, indent=None):
    """Convert object to JSON string."""
    try:
        if indent is not None:
            return json.dumps(obj, indent=int(indent))
        return json.dumps(obj)
    except Exception as e:
        raise ValueError(f"Cannot serialize to JSON: {e}")

def tombo_parse(json_str):
    """Parse JSON string."""
    try:
        return json.loads(str(json_str))
    except Exception as e:
        raise ValueError(f"Invalid JSON: {e}")

def tombo_encode(obj):
    """Encode object to JSON (alias for stringify)."""
    return tombo_stringify(obj)

def tombo_decode(json_str):
    """Decode JSON string (alias for parse)."""
    return tombo_parse(json_str)

def tombo_to_json(obj):
    """Convert to JSON string."""
    return tombo_stringify(obj)

def tombo_from_json(json_str):
    """Parse JSON string."""
    return tombo_parse(json_str)

def tombo_load(file_path):
    """Load JSON from file."""
    try:
        with open(str(file_path), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise IOError(f"Cannot load JSON file: {e}")

def tombo_loads(json_str):
    """Load JSON from string."""
    return tombo_parse(json_str)

def tombo_dump(obj, file_path, indent=None):
    """Dump object to JSON file."""
    try:
        with open(str(file_path), 'w', encoding='utf-8') as f:
            if indent is not None:
                json.dump(obj, f, indent=int(indent))
            else:
                json.dump(obj, f)
        return True
    except Exception as e:
        raise IOError(f"Cannot write JSON file: {e}")

def tombo_dumps(obj, indent=None):
    """Dump object to JSON string."""
    return tombo_stringify(obj, indent)

def tombo_validate(json_str):
    """Validate JSON string."""
    try:
        json.loads(str(json_str))
        return True
    except:
        return False

def tombo_prettify(json_str, indent=2):
    """Pretty print JSON."""
    try:
        obj = json.loads(str(json_str))
        return json.dumps(obj, indent=int(indent))
    except Exception as e:
        raise ValueError(f"Invalid JSON: {e}")

def tombo_minify(json_str):
    """Minify JSON."""
    try:
        obj = json.loads(str(json_str))
        return json.dumps(obj, separators=(',', ':'))
    except Exception as e:
        raise ValueError(f"Invalid JSON: {e}")

def tombo_keys(json_obj):
    """Get keys from JSON object."""
    if isinstance(json_obj, dict):
        return list(json_obj.keys())
    return []

def tombo_values(json_obj):
    """Get values from JSON object."""
    if isinstance(json_obj, dict):
        return list(json_obj.values())
    return []

def register(env):
    """Register JSON library functions."""
    functions = {
        'stringify': tombo_stringify,
        'parse': tombo_parse,
        'encode': tombo_encode,
        'decode': tombo_decode,
        'to_json': tombo_to_json,
        'from_json': tombo_from_json,
        'load': tombo_load,
        'loads': tombo_loads,
        'dump': tombo_dump,
        'dumps': tombo_dumps,
        'validate': tombo_validate,
        'prettify': tombo_prettify,
        'minify': tombo_minify,
        'keys': tombo_keys,
        'values': tombo_values,
    }
    for name, func in functions.items():
        env.set(name, func)
