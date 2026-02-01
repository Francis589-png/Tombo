"""
Run the stdlib demo to verify library integration with Tombo `.to` files
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.interpreter import Interpreter
from src.core.fs import run_file

print("=" * 70)
print("TOMBO STANDARD LIBRARY DEMO")
print("=" * 70)
print()

# Create interpreter and run the demo file
interp = Interpreter()
try:
    result = run_file('examples/stdlib_demo.to', interp)
    print()
    print("=" * 70)
    print("DEMO EXECUTED SUCCESSFULLY ✓")
    print("=" * 70)
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
