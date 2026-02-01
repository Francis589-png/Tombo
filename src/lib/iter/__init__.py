"""
Tombo Iter Library - Iteration Tools
"""
import itertools

def tombo_range(*args):
    """Create range iterator."""
    return list(range(*[int(a) for a in args]))

def tombo_enumerate(iterable, start=0):
    """Enumerate with index."""
    if isinstance(iterable, list):
        return [(i + int(start), v) for i, v in enumerate(iterable)]
    return []

def tombo_zip(*iterables):
    """Zip multiple iterables."""
    return list(zip(*iterables))

def tombo_map(func, iterable):
    """Map function over iterable."""
    if callable(func) and isinstance(iterable, list):
        return [func(x) for x in iterable]
    return []

def tombo_filter(func, iterable):
    """Filter iterable by function."""
    if callable(func) and isinstance(iterable, list):
        return [x for x in iterable if func(x)]
    return []

def tombo_reduce(func, iterable, initializer=None):
    """Reduce iterable."""
    if not isinstance(iterable, list) or not callable(func):
        return None
    
    if len(iterable) == 0:
        return initializer
    
    if initializer is not None:
        acc = initializer
        start = 0
    else:
        acc = iterable[0]
        start = 1
    
    for x in iterable[start:]:
        acc = func(acc, x)
    return acc

def tombo_chain(*iterables):
    """Chain iterables together."""
    result = []
    for it in iterables:
        if isinstance(it, list):
            result.extend(it)
    return result

def tombo_cycle(iterable, count=None):
    """Cycle through iterable."""
    if isinstance(iterable, list):
        result = []
        if count is None:
            return iterable * 3  # Default cycle
        for _ in range(int(count)):
            result.extend(iterable)
        return result
    return []

def tombo_repeat(obj, count=None):
    """Repeat object."""
    if count is None:
        return [obj] * 3
    return [obj] * int(count)

def tombo_slice(iterable, start, stop, step=1):
    """Slice iterable."""
    if isinstance(iterable, (list, str)):
        return iterable[int(start):int(stop):int(step)]
    return []

def tombo_takewhile(func, iterable):
    """Take elements while condition is true."""
    if callable(func) and isinstance(iterable, list):
        result = []
        for x in iterable:
            if func(x):
                result.append(x)
            else:
                break
        return result
    return []

def tombo_dropwhile(func, iterable):
    """Drop elements while condition is true."""
    if callable(func) and isinstance(iterable, list):
        dropping = True
        result = []
        for x in iterable:
            if dropping and func(x):
                continue
            dropping = False
            result.append(x)
        return result
    return []

def tombo_permutations(iterable, r=None):
    """Generate permutations."""
    if isinstance(iterable, list):
        if r is None:
            r = len(iterable)
        return [list(p) for p in itertools.permutations(iterable, int(r))]
    return []

def tombo_combinations(iterable, r):
    """Generate combinations."""
    if isinstance(iterable, list):
        return [list(c) for c in itertools.combinations(iterable, int(r))]
    return []

def tombo_combinations_with_replacement(iterable, r):
    """Generate combinations with replacement."""
    if isinstance(iterable, list):
        return [list(c) for c in itertools.combinations_with_replacement(iterable, int(r))]
    return []

def tombo_product(*iterables):
    """Cartesian product."""
    result = []
    for p in itertools.product(*iterables):
        result.append(list(p))
    return result

def register(env):
    """Register iter library functions."""
    functions = {
        'range': tombo_range,
        'enumerate': tombo_enumerate,
        'zip': tombo_zip,
        'map': tombo_map,
        'filter': tombo_filter,
        'reduce': tombo_reduce,
        'chain': tombo_chain,
        'cycle': tombo_cycle,
        'repeat': tombo_repeat,
        'slice': tombo_slice,
        'takewhile': tombo_takewhile,
        'dropwhile': tombo_dropwhile,
        'permutations': tombo_permutations,
        'combinations': tombo_combinations,
        'combinations_with_replacement': tombo_combinations_with_replacement,
        'product': tombo_product,
    }
    for name, func in functions.items():
        env.set(name, func)
