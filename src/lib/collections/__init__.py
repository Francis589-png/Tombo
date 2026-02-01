"""
Tombo Collections Library - Data Structure Operations
"""

# List operations
def tombo_append(lst, item):
    """Append item to list."""
    if isinstance(lst, list):
        lst.append(item)
    return lst

def tombo_extend(lst, items):
    """Extend list with items."""
    if isinstance(lst, list) and isinstance(items, list):
        lst.extend(items)
    return lst

def tombo_insert(lst, index, item):
    """Insert item at index."""
    if isinstance(lst, list):
        lst.insert(int(index), item)
    return lst

def tombo_remove(lst, item):
    """Remove item from list."""
    if isinstance(lst, list):
        lst.remove(item)
    return lst

def tombo_pop(lst, index=-1):
    """Pop item from list."""
    if isinstance(lst, list):
        return lst.pop(int(index))
    return None

def tombo_clear(lst):
    """Clear list."""
    if isinstance(lst, list):
        lst.clear()
    elif isinstance(lst, dict):
        lst.clear()
    elif isinstance(lst, set):
        lst.clear()
    return lst

def tombo_index(lst, item, start=0):
    """Find index of item."""
    if isinstance(lst, list):
        return lst.index(item, int(start))
    return -1

def tombo_count(lst, item):
    """Count occurrences of item."""
    if isinstance(lst, list):
        return lst.count(item)
    return 0

def tombo_sort(lst, reverse=False):
    """Sort list."""
    if isinstance(lst, list):
        lst.sort(reverse=reverse)
    return lst

def tombo_reverse(lst):
    """Reverse list."""
    if isinstance(lst, list):
        lst.reverse()
    return lst

def tombo_slice(lst, start=0, end=None, step=1):
    """Slice list."""
    if isinstance(lst, (list, str)):
        start = int(start)
        end = int(end) if end is not None else None
        step = int(step)
        return lst[start:end:step]
    return lst

def tombo_chunk(lst, size):
    """Split list into chunks."""
    if not isinstance(lst, list):
        return []
    size = int(size)
    return [lst[i:i+size] for i in range(0, len(lst), size)]

def tombo_flatten(lst, depth=None):
    """Flatten nested list."""
    if not isinstance(lst, list):
        return lst
    if depth is None:
        depth = float('inf')
    depth = int(depth) if isinstance(depth, float) and depth != float('inf') else float('inf')
    
    def _flatten(l, d):
        result = []
        for item in l:
            if isinstance(item, list) and d > 0:
                result.extend(_flatten(item, d - 1))
            else:
                result.append(item)
        return result
    
    return _flatten(lst, depth)

def tombo_zip(*lists):
    """Zip multiple lists together."""
    return list(zip(*lists))

def tombo_enumerate(lst, start=0):
    """Enumerate list with indices."""
    if isinstance(lst, list):
        return [(i + int(start), v) for i, v in enumerate(lst)]
    return []

# Dictionary operations
def tombo_keys(d):
    """Get dictionary keys."""
    if isinstance(d, dict):
        return list(d.keys())
    return []

def tombo_values(d):
    """Get dictionary values."""
    if isinstance(d, dict):
        return list(d.values())
    return []

def tombo_items(d):
    """Get dictionary items as key-value pairs."""
    if isinstance(d, dict):
        return [[k, v] for k, v in d.items()]
    return []

def tombo_get(d, key, default=None):
    """Get value with default."""
    if isinstance(d, dict):
        return d.get(str(key), default)
    return default

def tombo_update(d, other):
    """Update dictionary."""
    if isinstance(d, dict) and isinstance(other, dict):
        d.update(other)
    return d

def tombo_merge(*dicts):
    """Merge multiple dictionaries."""
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result

def tombo_invert(d):
    """Invert dictionary (swap keys and values)."""
    if isinstance(d, dict):
        return {str(v): k for k, v in d.items()}
    return {}

def tombo_filter_keys(d, predicate):
    """Filter dictionary by keys."""
    if isinstance(d, dict) and callable(predicate):
        return {k: v for k, v in d.items() if predicate(k)}
    return {}

def tombo_filter_values(d, predicate):
    """Filter dictionary by values."""
    if isinstance(d, dict) and callable(predicate):
        return {k: v for k, v in d.items() if predicate(v)}
    return {}

# Set operations
def tombo_union(s1, s2):
    """Union of two sets."""
    if isinstance(s1, (set, list)) and isinstance(s2, (set, list)):
        s1 = set(s1) if isinstance(s1, list) else s1
        s2 = set(s2) if isinstance(s2, list) else s2
        return list(s1.union(s2))
    return []

def tombo_intersection(s1, s2):
    """Intersection of two sets."""
    if isinstance(s1, (set, list)) and isinstance(s2, (set, list)):
        s1 = set(s1) if isinstance(s1, list) else s1
        s2 = set(s2) if isinstance(s2, list) else s2
        return list(s1.intersection(s2))
    return []

def tombo_difference(s1, s2):
    """Difference of two sets."""
    if isinstance(s1, (set, list)) and isinstance(s2, (set, list)):
        s1 = set(s1) if isinstance(s1, list) else s1
        s2 = set(s2) if isinstance(s2, list) else s2
        return list(s1.difference(s2))
    return []

def tombo_symmetric_difference(s1, s2):
    """Symmetric difference of two sets."""
    if isinstance(s1, (set, list)) and isinstance(s2, (set, list)):
        s1 = set(s1) if isinstance(s1, list) else s1
        s2 = set(s2) if isinstance(s2, list) else s2
        return list(s1.symmetric_difference(s2))
    return []

def tombo_add(s, item):
    """Add item to set."""
    if isinstance(s, set):
        s.add(item)
    elif isinstance(s, list):
        if item not in s:
            s.append(item)
    return s

def tombo_discard(s, item):
    """Discard item from set."""
    if isinstance(s, set):
        s.discard(item)
    elif isinstance(s, list):
        try:
            s.remove(item)
        except ValueError:
            pass
    return s

def tombo_is_subset(s1, s2):
    """Check if s1 is subset of s2."""
    if isinstance(s1, (set, list)) and isinstance(s2, (set, list)):
        s1 = set(s1) if isinstance(s1, list) else s1
        s2 = set(s2) if isinstance(s2, list) else s2
        return s1.issubset(s2)
    return False

def tombo_is_superset(s1, s2):
    """Check if s1 is superset of s2."""
    if isinstance(s1, (set, list)) and isinstance(s2, (set, list)):
        s1 = set(s1) if isinstance(s1, list) else s1
        s2 = set(s2) if isinstance(s2, list) else s2
        return s1.issuperset(s2)
    return False

# Tuple operations
def tombo_first(seq):
    """Get first element."""
    if isinstance(seq, (list, tuple, str)) and len(seq) > 0:
        return seq[0]
    return None

def tombo_last(seq):
    """Get last element."""
    if isinstance(seq, (list, tuple, str)) and len(seq) > 0:
        return seq[-1]
    return None

def register(env):
    """Register collections library functions in the interpreter environment."""
    functions = {
        # List operations
        'append': tombo_append,
        'extend': tombo_extend,
        'insert': tombo_insert,
        'remove': tombo_remove,
        'pop': tombo_pop,
        'clear': tombo_clear,
        'index': tombo_index,
        'count': tombo_count,
        'sort': tombo_sort,
        'reverse': tombo_reverse,
        'slice': tombo_slice,
        'chunk': tombo_chunk,
        'flatten': tombo_flatten,
        'zip': tombo_zip,
        'enumerate': tombo_enumerate,
        
        # Dictionary operations
        'keys': tombo_keys,
        'values': tombo_values,
        'items': tombo_items,
        'get': tombo_get,
        'update': tombo_update,
        'merge': tombo_merge,
        'invert': tombo_invert,
        'filter_keys': tombo_filter_keys,
        'filter_values': tombo_filter_values,
        
        # Set operations
        'union': tombo_union,
        'intersection': tombo_intersection,
        'difference': tombo_difference,
        'symmetric_difference': tombo_symmetric_difference,
        'add': tombo_add,
        'discard': tombo_discard,
        'is_subset': tombo_is_subset,
        'is_superset': tombo_is_superset,
        
        # Tuple/sequence operations
        'first': tombo_first,
        'last': tombo_last,
    }
    
    for name, func in functions.items():
        env.set(name, func)
