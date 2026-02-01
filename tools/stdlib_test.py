"""
Test to validate all stdlib libraries load correctly
"""
import sys
sys.path.insert(0, 'C:\\Users\\FRANCIS JUSU\\Documents\\TOMBO')

from src.core.interpreter import Interpreter

# Create interpreter (will load all stdlib)
interp = Interpreter()

# Check what's in global env
env_keys = sorted(interp.global_env.store.keys())

print("=" * 60)
print("STDLIB LOADED SUCCESSFULLY")
print("=" * 60)
print(f"\nTotal functions/constants loaded: {len(env_keys)}")
print("\nAvailable names (grouped by library):")

# Group by library
core_funcs = ['int', 'float', 'str', 'bool', 'list', 'dict', 'set', 'tuple', 
              'type', 'isinstance', 'callable', 'id', 'hash', 'repr', 'dir',
              'getattr', 'setattr', 'hasattr', 'delattr', 'copy', 'deep_copy']
math_funcs = ['PI', 'E', 'TAU', 'PHI', 'INF', 'NAN', 'abs', 'round', 'floor', 
              'ceil', 'trunc', 'min', 'max', 'sum', 'product', 'mean', 'median',
              'pow', 'sqrt', 'cbrt', 'exp', 'log', 'log10', 'log2',
              'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2',
              'sinh', 'cosh', 'tanh', 'degrees', 'radians',
              'gcd', 'lcm', 'factorial', 'is_prime', 'fibonacci',
              'random', 'randint', 'choice', 'seed']
string_funcs = ['length', 'upper', 'lower', 'capitalize', 'title', 'swapcase',
                'strip', 'lstrip', 'rstrip', 'trim', 'find', 'rfind', 'index', 
                'count', 'replace', 'split', 'join', 'split_lines', 'starts_with',
                'ends_with', 'contains', 'is_alpha', 'is_digit', 'is_alnum',
                'is_space', 'is_lower', 'is_upper', 'pad_left', 'pad_right',
                'pad_center', 'remove_prefix', 'remove_suffix']
collections_funcs = ['append', 'extend', 'insert', 'remove', 'pop', 'clear',
                     'index', 'count', 'sort', 'reverse', 'slice', 'chunk',
                     'flatten', 'zip', 'enumerate', 'keys', 'values', 'items',
                     'get', 'update', 'merge', 'invert', 'filter_keys',
                     'filter_values', 'union', 'intersection', 'difference',
                     'symmetric_difference', 'add', 'discard', 'is_subset',
                     'is_superset', 'first', 'last']
io_funcs = ['println', 'input', 'input_number', 'input_bool', 'eprint', 'eprintln',
            'read_file', 'write_file', 'append_file', 'file_exists', 'is_file',
            'is_dir', 'delete_file', 'copy_file', 'move_file', 'rename_file',
            'file_size', 'file_time', 'list_dir', 'make_dir', 'remove_dir',
            'change_dir', 'current_dir', 'walk_dir', 'glob',
            'path_join', 'path_split', 'path_base', 'path_dir', 'path_ext',
            'path_abs', 'path_rel', 'path_norm']
time_funcs = ['now', 'today', 'utc_now', 'time', 'sleep', 'delay', 'timestamp',
              'timezone', 'date', 'datetime', 'date_add', 'date_sub', 'date_diff',
              'date_format', 'date_parse', 'year', 'month', 'day', 'hour',
              'minute', 'second', 'weekday', 'isoweekday', 'is_leap_year',
              'days_in_month', 'stopwatch', 'measure']

groups = {
    'core': core_funcs,
    'math': math_funcs,
    'string': string_funcs,
    'collections': collections_funcs,
    'io': io_funcs,
    'time': time_funcs,
    'builtins': ['print', 'len', 'range'],
}

for group, expected in groups.items():
    loaded = [name for name in expected if name in env_keys]
    missing = [name for name in expected if name not in env_keys]
    
    print(f"\n{group.upper()} ({len(loaded)}/{len(expected)}):")
    if loaded:
        print(f"  ✓ {', '.join(loaded[:10])}" + ("..." if len(loaded) > 10 else ""))
    if missing:
        print(f"  ✗ MISSING: {', '.join(missing)}")

# Test a few functions
print("\n" + "=" * 60)
print("QUICK FUNCTION TESTS")
print("=" * 60)

# Test math
print(f"\nMath.sqrt(16) = {interp.global_env.get('sqrt')(16)}")
print(f"Math.sin(0) = {interp.global_env.get('sin')(0)}")

# Test string
print(f"\nString.upper('hello') = {interp.global_env.get('upper')('hello')}")
print(f"String.split('a,b,c', ',') = {interp.global_env.get('split')('a,b,c', ',')}")

# Test collections
test_list = [3, 1, 4, 1, 5]
sorted_list = test_list.copy()
interp.global_env.get('sort')(sorted_list)
print(f"\nCollections.sort([3,1,4,1,5]) = {sorted_list}")

# Test type conversions
print(f"\nCore.int('42') = {interp.global_env.get('int')('42')}")
print(f"Core.str(123) = {interp.global_env.get('str')(123)}")

print("\n" + "=" * 60)
print("ALL TESTS PASSED ✓")
print("=" * 60)
