#!/usr/bin/env python
"""
Check if println is loaded
"""
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.interpreter import Interpreter

interp = Interpreter()

# Check for println
println_fn = interp.global_env.get('println')
print(f"println function: {println_fn}")
print(f"println type: {type(println_fn)}")

if callable(println_fn):
    print("\nCalling println('TEST'):")
    println_fn("TEST")
    print("(after call)")

# Check print too
print_fn = interp.global_env.get('print')
print(f"\nprint function: {print_fn}")
if callable(print_fn):
    print("Calling print('HELLO'):")
    print_fn("HELLO")
