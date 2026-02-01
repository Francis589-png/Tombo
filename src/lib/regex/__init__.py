"""
Tombo Regex Library - Regular Expression Operations
"""
import re

def tombo_compile(pattern, flags=0):
    """Compile a regex pattern."""
    try:
        return re.compile(str(pattern), int(flags))
    except Exception as e:
        raise ValueError(f"Invalid regex pattern: {e}")

def tombo_match(pattern, string, flags=0):
    """Check if pattern matches at start of string."""
    try:
        return re.match(str(pattern), str(string), int(flags)) is not None
    except Exception as e:
        raise ValueError(f"Regex error: {e}")

def tombo_search(pattern, string, flags=0):
    """Search for pattern anywhere in string."""
    try:
        m = re.search(str(pattern), str(string), int(flags))
        return m is not None
    except Exception as e:
        raise ValueError(f"Regex error: {e}")

def tombo_find_all(pattern, string, flags=0):
    """Find all matches of pattern."""
    try:
        return re.findall(str(pattern), str(string), int(flags))
    except Exception as e:
        raise ValueError(f"Regex error: {e}")

def tombo_find_iter(pattern, string, flags=0):
    """Iterate over matches."""
    try:
        return list(re.finditer(str(pattern), str(string), int(flags)))
    except Exception as e:
        raise ValueError(f"Regex error: {e}")

def tombo_split(pattern, string, maxsplit=0, flags=0):
    """Split string by pattern."""
    try:
        return re.split(str(pattern), str(string), int(maxsplit), int(flags))
    except Exception as e:
        raise ValueError(f"Regex error: {e}")

def tombo_sub(pattern, repl, string, count=0, flags=0):
    """Substitute matches."""
    try:
        return re.sub(str(pattern), str(repl), str(string), int(count), int(flags))
    except Exception as e:
        raise ValueError(f"Regex error: {e}")

def tombo_subn(pattern, repl, string, count=0, flags=0):
    """Substitute matches and return count."""
    try:
        result, n = re.subn(str(pattern), str(repl), str(string), int(count), int(flags))
        return [result, n]
    except Exception as e:
        raise ValueError(f"Regex error: {e}")

def tombo_escape(pattern):
    """Escape special regex characters."""
    return re.escape(str(pattern))

def tombo_group(match_obj, group_num=0):
    """Get group from match object."""
    if hasattr(match_obj, 'group'):
        return match_obj.group(int(group_num))
    return None

def tombo_groups(match_obj):
    """Get all groups from match object."""
    if hasattr(match_obj, 'groups'):
        return match_obj.groups()
    return []

def tombo_start(match_obj):
    """Get start position of match."""
    if hasattr(match_obj, 'start'):
        return match_obj.start()
    return -1

def tombo_end(match_obj):
    """Get end position of match."""
    if hasattr(match_obj, 'end'):
        return match_obj.end()
    return -1

def register(env):
    """Register regex library functions."""
    functions = {
        'compile': tombo_compile,
        'match': tombo_match,
        'search': tombo_search,
        'find_all': tombo_find_all,
        'find_iter': tombo_find_iter,
        'split': tombo_split,
        'sub': tombo_sub,
        'subn': tombo_subn,
        'escape': tombo_escape,
        'group': tombo_group,
        'groups': tombo_groups,
        'start': tombo_start,
        'end': tombo_end,
    }
    for name, func in functions.items():
        env.set(name, func)
