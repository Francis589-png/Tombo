"""
Tombo Functools Library - Functional Programming Tools
"""

def tombo_partial(func, *args):
    """Create partial function."""
    if callable(func):
        def wrapper(*more_args):
            return func(*(args + more_args))
        return wrapper
    return func

def tombo_compose(*functions):
    """Compose functions right-to-left."""
    def wrapper(x):
        result = x
        for f in reversed(functions):
            if callable(f):
                result = f(result)
        return result
    return wrapper

def tombo_pipe(*functions):
    """Pipe functions left-to-right."""
    def wrapper(x):
        result = x
        for f in functions:
            if callable(f):
                result = f(result)
        return result
    return wrapper

def tombo_memoize(func):
    """Memoize function results."""
    if not callable(func):
        return func
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

def tombo_lru_cache(maxsize=128):
    """LRU cache decorator."""
    def decorator(func):
        if not callable(func):
            return func
        cache = {}
        order = []
        def wrapper(*args):
            if args in cache:
                order.remove(args)
                order.append(args)
                return cache[args]
            if len(cache) >= maxsize:
                oldest = order.pop(0)
                del cache[oldest]
            result = func(*args)
            cache[args] = result
            order.append(args)
            return result
        return wrapper
    return decorator

def tombo_retry(times=3, delay=0):
    """Retry decorator."""
    def decorator(func):
        if not callable(func):
            return func
        def wrapper(*args):
            import time
            for attempt in range(int(times)):
                try:
                    return func(*args)
                except Exception as e:
                    if attempt == int(times) - 1:
                        raise
                    time.sleep(float(delay))
            return None
        return wrapper
    return decorator

def tombo_throttle(seconds=1):
    """Throttle function calls."""
    import time
    last_called = [0]
    def decorator(func):
        if not callable(func):
            return func
        def wrapper(*args):
            now = time.time()
            if now - last_called[0] >= float(seconds):
                last_called[0] = now
                return func(*args)
            return None
        return wrapper
    return decorator

def tombo_debounce(seconds=1):
    """Debounce function calls."""
    import time
    timer = [None]
    def decorator(func):
        if not callable(func):
            return func
        def wrapper(*args):
            if timer[0]:
                # Cancel previous timer
                pass
            def delayed():
                func(*args)
            timer[0] = delayed
            # Simulate timing
            return None
        return wrapper
    return decorator

def tombo_singleton(cls):
    """Make class a singleton."""
    instances = {}
    def get_instance(*args):
        if cls not in instances:
            instances[cls] = cls(*args)
        return instances[cls]
    return get_instance

def tombo_curry(func, arity=None):
    """Curry function."""
    if not callable(func):
        return func
    if arity is None:
        arity = func.__code__.co_argcount
    
    def curried(*args):
        if len(args) >= arity:
            return func(*args[:arity])
        return partial(curried, *args)
    return curried

def tombo_uncurry(func):
    """Uncurry function."""
    def wrapper(*args):
        result = func
        for arg in args:
            if callable(result):
                result = result(arg)
        return result
    return wrapper

def tombo_once(func):
    """Call function only once."""
    called = [False]
    result = [None]
    def wrapper(*args):
        if not called[0]:
            called[0] = True
            result[0] = func(*args)
        return result[0]
    return wrapper

def register(env):
    """Register functools library functions."""
    functions = {
        'partial': tombo_partial,
        'compose': tombo_compose,
        'pipe': tombo_pipe,
        'memoize': tombo_memoize,
        'lru_cache': tombo_lru_cache,
        'retry': tombo_retry,
        'throttle': tombo_throttle,
        'debounce': tombo_debounce,
        'singleton': tombo_singleton,
        'curry': tombo_curry,
        'uncurry': tombo_uncurry,
        'once': tombo_once,
    }
    for name, func in functions.items():
        env.set(name, func)
