"""
Tombo Math Library - Mathematical Functions and Constants
"""
import math as py_math

# Mathematical constants
PI = py_math.pi
E = py_math.e
TAU = 2 * py_math.pi
PHI = (1 + py_math.sqrt(5)) / 2
INF = float('inf')
NAN = float('nan')

# Basic operations
def tombo_abs(x):
    """Absolute value."""
    return abs(x)

def tombo_round(x, ndigits=0):
    """Round to nearest integer or to n decimal places."""
    if ndigits == 0:
        return round(x)
    return round(x, int(ndigits))

def tombo_floor(x):
    """Floor function."""
    return py_math.floor(x)

def tombo_ceil(x):
    """Ceiling function."""
    return py_math.ceil(x)

def tombo_trunc(x):
    """Truncate to integer."""
    return py_math.trunc(x)

def tombo_min(*args):
    """Minimum of arguments."""
    if len(args) == 1 and isinstance(args[0], list):
        return min(args[0])
    return min(args) if args else None

def tombo_max(*args):
    """Maximum of arguments."""
    if len(args) == 1 and isinstance(args[0], list):
        return max(args[0])
    return max(args) if args else None

def tombo_sum(iterable, start=0):
    """Sum of elements."""
    if isinstance(iterable, list):
        return sum(iterable) + start
    return iterable + start

def tombo_product(*args):
    """Product of arguments."""
    if len(args) == 1 and isinstance(args[0], list):
        args = args[0]
    result = 1
    for x in args:
        result *= x
    return result

def tombo_mean(values):
    """Mean/average of values."""
    if not isinstance(values, list) or len(values) == 0:
        return 0
    return sum(values) / len(values)

def tombo_median(values):
    """Median of values."""
    if not isinstance(values, list) or len(values) == 0:
        return 0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n % 2 == 0:
        return (sorted_vals[n//2 - 1] + sorted_vals[n//2]) / 2
    return sorted_vals[n//2]

# Power and logarithms
def tombo_pow(x, y):
    """Power function x^y."""
    return pow(x, y)

def tombo_sqrt(x):
    """Square root."""
    if x < 0:
        raise ValueError("Cannot take square root of negative number")
    return py_math.sqrt(x)

def tombo_cbrt(x):
    """Cube root."""
    if x < 0:
        return -(-x) ** (1/3)
    return x ** (1/3)

def tombo_exp(x):
    """e^x."""
    return py_math.exp(x)

def tombo_log(x, base=py_math.e):
    """Logarithm with optional base."""
    if x <= 0:
        raise ValueError("Cannot take logarithm of non-positive number")
    if base == py_math.e:
        return py_math.log(x)
    return py_math.log(x, base)

def tombo_log10(x):
    """Base 10 logarithm."""
    if x <= 0:
        raise ValueError("Cannot take logarithm of non-positive number")
    return py_math.log10(x)

def tombo_log2(x):
    """Base 2 logarithm."""
    if x <= 0:
        raise ValueError("Cannot take logarithm of non-positive number")
    return py_math.log2(x)

# Trigonometry
def tombo_sin(x):
    """Sine (x in radians)."""
    return py_math.sin(x)

def tombo_cos(x):
    """Cosine (x in radians)."""
    return py_math.cos(x)

def tombo_tan(x):
    """Tangent (x in radians)."""
    return py_math.tan(x)

def tombo_asin(x):
    """Arcsine."""
    if x < -1 or x > 1:
        raise ValueError("asin domain error")
    return py_math.asin(x)

def tombo_acos(x):
    """Arccosine."""
    if x < -1 or x > 1:
        raise ValueError("acos domain error")
    return py_math.acos(x)

def tombo_atan(x):
    """Arctangent."""
    return py_math.atan(x)

def tombo_atan2(y, x):
    """Two-argument arctangent."""
    return py_math.atan2(y, x)

def tombo_sinh(x):
    """Hyperbolic sine."""
    return py_math.sinh(x)

def tombo_cosh(x):
    """Hyperbolic cosine."""
    return py_math.cosh(x)

def tombo_tanh(x):
    """Hyperbolic tangent."""
    return py_math.tanh(x)

def tombo_degrees(x):
    """Convert radians to degrees."""
    return py_math.degrees(x)

def tombo_radians(x):
    """Convert degrees to radians."""
    return py_math.radians(x)

# Number theory
def tombo_gcd(*args):
    """Greatest common divisor."""
    if len(args) == 1 and isinstance(args[0], list):
        args = args[0]
    result = abs(int(args[0])) if args else 0
    for x in args[1:]:
        result = py_math.gcd(result, abs(int(x)))
    return result

def tombo_lcm(*args):
    """Least common multiple."""
    if len(args) == 1 and isinstance(args[0], list):
        args = args[0]
    if not args:
        return 1
    result = abs(int(args[0]))
    for x in args[1:]:
        x = abs(int(x))
        result = result * x // py_math.gcd(result, x)
    return result

def tombo_factorial(n):
    """Factorial."""
    return py_math.factorial(int(n))

def tombo_is_prime(n):
    """Check if n is prime."""
    n = int(n)
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(py_math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def tombo_fibonacci(n):
    """Get nth Fibonacci number."""
    n = int(n)
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Random
def tombo_random():
    """Random float [0.0, 1.0)."""
    import random
    return random.random()

def tombo_randint(a, b):
    """Random integer [a, b]."""
    import random
    return random.randint(int(a), int(b))

def tombo_choice(seq):
    """Random choice from sequence."""
    import random
    return random.choice(seq)

def tombo_seed(s=None):
    """Set random seed."""
    import random
    random.seed(s)
    return None

def register(env):
    """Register math library functions in the interpreter environment."""
    # Constants
    env.set('PI', PI)
    env.set('E', E)
    env.set('TAU', TAU)
    env.set('PHI', PHI)
    env.set('INF', INF)
    env.set('NAN', NAN)
    
    # Functions
    functions = {
        # Basic operations
        'abs': tombo_abs,
        'round': tombo_round,
        'floor': tombo_floor,
        'ceil': tombo_ceil,
        'trunc': tombo_trunc,
        'min': tombo_min,
        'max': tombo_max,
        'sum': tombo_sum,
        'product': tombo_product,
        'mean': tombo_mean,
        'median': tombo_median,
        
        # Power and logarithms
        'pow': tombo_pow,
        'sqrt': tombo_sqrt,
        'cbrt': tombo_cbrt,
        'exp': tombo_exp,
        'log': tombo_log,
        'log10': tombo_log10,
        'log2': tombo_log2,
        
        # Trigonometry
        'sin': tombo_sin,
        'cos': tombo_cos,
        'tan': tombo_tan,
        'asin': tombo_asin,
        'acos': tombo_acos,
        'atan': tombo_atan,
        'atan2': tombo_atan2,
        'sinh': tombo_sinh,
        'cosh': tombo_cosh,
        'tanh': tombo_tanh,
        'degrees': tombo_degrees,
        'radians': tombo_radians,
        
        # Number theory
        'gcd': tombo_gcd,
        'lcm': tombo_lcm,
        'factorial': tombo_factorial,
        'is_prime': tombo_is_prime,
        'fibonacci': tombo_fibonacci,
        
        # Random
        'random': tombo_random,
        'randint': tombo_randint,
        'choice': tombo_choice,
        'seed': tombo_seed,
    }
    
    for name, func in functions.items():
        env.set(name, func)
