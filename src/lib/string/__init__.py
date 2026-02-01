"""
Tombo String Library - String Manipulation and Formatting
"""

def tombo_length(s):
    """Get string length."""
    return len(str(s))

def tombo_upper(s):
    """Convert to uppercase."""
    return str(s).upper()

def tombo_lower(s):
    """Convert to lowercase."""
    return str(s).lower()

def tombo_capitalize(s):
    """Capitalize first character."""
    return str(s).capitalize()

def tombo_title(s):
    """Title case."""
    return str(s).title()

def tombo_swapcase(s):
    """Swap case."""
    return str(s).swapcase()

def tombo_strip(s, chars=None):
    """Strip leading and trailing whitespace."""
    s = str(s)
    if chars is None:
        return s.strip()
    return s.strip(chars)

def tombo_lstrip(s, chars=None):
    """Strip leading whitespace."""
    s = str(s)
    if chars is None:
        return s.lstrip()
    return s.lstrip(chars)

def tombo_rstrip(s, chars=None):
    """Strip trailing whitespace."""
    s = str(s)
    if chars is None:
        return s.rstrip()
    return s.rstrip(chars)

def tombo_trim(s):
    """Trim whitespace (alias for strip)."""
    return str(s).strip()

# Search and replace
def tombo_find(s, sub, start=0):
    """Find substring position."""
    return str(s).find(str(sub), int(start))

def tombo_rfind(s, sub, start=0):
    """Find substring from right."""
    return str(s).rfind(str(sub), int(start))

def tombo_index(s, sub, start=0):
    """Find substring index (raises error if not found)."""
    s = str(s)
    sub = str(sub)
    idx = s.find(sub, int(start))
    if idx == -1:
        raise ValueError(f"Substring '{sub}' not found in string")
    return idx

def tombo_count(s, sub):
    """Count occurrences of substring."""
    return str(s).count(str(sub))

def tombo_replace(s, old, new, count=-1):
    """Replace substring."""
    if count == -1:
        return str(s).replace(str(old), str(new))
    return str(s).replace(str(old), str(new), int(count))

# Splitting and joining
def tombo_split(s, sep=None, maxsplit=-1):
    """Split string."""
    s = str(s)
    if sep is None:
        if maxsplit == -1:
            return s.split()
        return s.split(maxsplit=int(maxsplit))
    if maxsplit == -1:
        return s.split(str(sep))
    return s.split(str(sep), int(maxsplit))

def tombo_join(sep, items):
    """Join list of strings."""
    sep = str(sep)
    if not isinstance(items, list):
        items = [items]
    return sep.join(str(item) for item in items)

def tombo_split_lines(s):
    """Split into lines."""
    return str(s).splitlines()

def tombo_startswith(s, prefix):
    """Check if starts with prefix."""
    return str(s).startswith(str(prefix))

def tombo_endswith(s, suffix):
    """Check if ends with suffix."""
    return str(s).endswith(str(suffix))

def tombo_contains(s, sub):
    """Check if contains substring."""
    return str(sub) in str(s)

# Character checking
def tombo_is_alpha(s):
    """Check if all alphabetic."""
    return str(s).isalpha()

def tombo_is_digit(s):
    """Check if all digits."""
    return str(s).isdigit()

def tombo_is_alnum(s):
    """Check if alphanumeric."""
    return str(s).isalnum()

def tombo_is_space(s):
    """Check if all whitespace."""
    return str(s).isspace()

def tombo_is_lower(s):
    """Check if all lowercase."""
    return str(s).islower()

def tombo_is_upper(s):
    """Check if all uppercase."""
    return str(s).isupper()

# Formatting
def tombo_pad_left(s, width, fill=' '):
    """Pad left with character."""
    s = str(s)
    fill = str(fill)[0] if fill else ' '
    return s.rjust(int(width), fill)

def tombo_pad_right(s, width, fill=' '):
    """Pad right with character."""
    s = str(s)
    fill = str(fill)[0] if fill else ' '
    return s.ljust(int(width), fill)

def tombo_pad_center(s, width, fill=' '):
    """Pad center with character."""
    s = str(s)
    fill = str(fill)[0] if fill else ' '
    return s.center(int(width), fill)

def tombo_remove_prefix(s, prefix):
    """Remove prefix if present."""
    s = str(s)
    prefix = str(prefix)
    if s.startswith(prefix):
        return s[len(prefix):]
    return s

def tombo_remove_suffix(s, suffix):
    """Remove suffix if present."""
    s = str(s)
    suffix = str(suffix)
    if s.endswith(suffix):
        return s[:-len(suffix)]
    return s

def register(env):
    """Register string library functions in the interpreter environment."""
    functions = {
        # Basic operations
        'length': tombo_length,
        'upper': tombo_upper,
        'lower': tombo_lower,
        'capitalize': tombo_capitalize,
        'title': tombo_title,
        'swapcase': tombo_swapcase,
        'strip': tombo_strip,
        'lstrip': tombo_lstrip,
        'rstrip': tombo_rstrip,
        'trim': tombo_trim,
        
        # Search and replace
        'find': tombo_find,
        'rfind': tombo_rfind,
        'index': tombo_index,
        'count': tombo_count,
        'replace': tombo_replace,
        
        # Splitting and joining
        'split': tombo_split,
        'join': tombo_join,
        'split_lines': tombo_split_lines,
        'starts_with': tombo_startswith,
        'ends_with': tombo_endswith,
        'contains': tombo_contains,
        
        # Character checking
        'is_alpha': tombo_is_alpha,
        'is_digit': tombo_is_digit,
        'is_alnum': tombo_is_alnum,
        'is_space': tombo_is_space,
        'is_lower': tombo_is_lower,
        'is_upper': tombo_is_upper,
        
        # Formatting
        'pad_left': tombo_pad_left,
        'pad_right': tombo_pad_right,
        'pad_center': tombo_pad_center,
        'remove_prefix': tombo_remove_prefix,
        'remove_suffix': tombo_remove_suffix,
    }
    
    for name, func in functions.items():
        env.set(name, func)
