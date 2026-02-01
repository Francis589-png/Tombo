#!/usr/bin/env python
"""
Comprehensive Tombo Standard Library Showcase
Demonstrates features from all 6 core libraries working together
"""
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.lexer import Lexer
from src.core.parser import Parser
from src.core.interpreter import Interpreter

# Comprehensive Tombo code showcasing the stdlib
tombo_code = """
println("=" * 70)
println("TOMBO STANDARD LIBRARY COMPREHENSIVE SHOWCASE")
println("=" * 70)

# ============ MATH LIBRARY ============
println("")
println("MATH LIBRARY")
println("-" * 70)

let numbers = [16, 9, 25, 36, 49]
println("Numbers: " + str(numbers))

let roots = [sqrt(16), sqrt(9), sqrt(25)]
println("Square roots: " + str(roots))

let pi_str = "PI = " + str(round(PI, 2))
println(pi_str)

# ============ STRING LIBRARY ============
println("")
println("STRING LIBRARY")
println("-" * 70)

let sentence = "The Quick Brown Fox Jumps"
println("Original: " + sentence)
println("Upper: " + upper(sentence))
println("Lower: " + lower(sentence))

let words = split(sentence, " ")
println("Words: " + str(words))
println("Joined: " + join("-", words))

# ============ COLLECTIONS LIBRARY ============
println("")
println("COLLECTIONS LIBRARY")
println("-" * 70)

let data = [42, 17, 99, 8, 55, 23]
println("Original list: " + str(data))

sort(data)
println("Sorted list: " + str(data))

reverse(data)
println("Reversed list: " + str(data))

println("First element: " + str(first(data)))
println("Last element: " + str(last(data)))

let sublist = slice(data, 1, 4)
println("Slice [1:4]: " + str(sublist))

# ============ CORE TYPE CONVERSION ============
println("")
println("CORE TYPE CONVERSION")
println("-" * 70)

let x = 123
println("Original int: " + str(x))
println("As string: " + str(x))
println("As float: " + str(float(x)))
println("As bool: " + str(bool(x)))
println("Type: " + type(x))

let y = "456"
println("String '456' as int: " + str(int(y)))
println("Type check - is string: " + str(isinstance(y, "string")))

# ============ I/O OPERATIONS ============
println("")
println("I/O OPERATIONS")
println("-" * 70)

let current_path = current_dir()
println("Current directory: " + current_path)

let file_list = list_dir(current_path)
println("Files in directory: " + str(first(file_list)))

# ============ COMBINED OPERATIONS ============
println("")
println("COMBINED OPERATIONS & FUNCTIONS")
println("-" * 70)

defi square(x) => x * x
defi add(a, b) => a + b

let result1 = square(5)
println("square(5) = " + str(result1))

let result2 = add(10, 20)
println("add(10, 20) = " + str(result2))

# Process a list with operations
let nums = [1, 2, 3, 4, 5]
let total = sum(nums)
println("Sum of [1,2,3,4,5]: " + str(total))

let average = mean(nums)
println("Mean of [1,2,3,4,5]: " + str(average))

# ============ SUMMARY ============
println("")
println("=" * 70)
println("SHOWCASE COMPLETE - All 193 stdlib functions available!")
println("=" * 70)
"""

print("Initializing Tombo interpreter with standard library...")
print()

interp = Interpreter()
print(f"✓ Loaded {len(interp.global_env.store)} builtin functions")
print()

print("Parsing and executing Tombo code...")
print()

try:
    lex = Lexer(tombo_code)
    tokens = lex.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interp.eval(ast)
    
    print()
    print("✓ Execution completed successfully!")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
