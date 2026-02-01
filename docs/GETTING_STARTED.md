# Tombo Language - Getting Started Guide

**Version:** 1.0.0  
**Date:** January 31, 2026  
**Difficulty:** Beginner to Intermediate

---

## Table of Contents

1. [Installation](#installation)
2. [Your First Program](#your-first-program)
3. [Basic Syntax](#basic-syntax)
4. [Working with Data](#working-with-data)
5. [Control Flow](#control-flow)
6. [Functions](#functions)
7. [Using Libraries](#using-libraries)
8. [Common Patterns](#common-patterns)
9. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites

- Python 3.8+
- pip or poetry

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd tombo-language
```

### Step 2: Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using poetry
poetry install
```

### Step 3: Verify Installation

```bash
python test_lexer_quick.py
python test_parser_quick.py
```

Both should complete without errors.

---

## Your First Program

### Hello World

Create a file named `hello.to`:

```tombo
println("Hello, World!")
```

Run it:

```bash
python -m src.main hello.to
```

Expected output:
```
Hello, World!
```

### Interactive REPL

Start the interactive interpreter:

```bash
python -m src.repl
```

You'll see:
```
Tombo REPL v1.0.0
> 
```

Type commands:
```
> println("Hello!")
Hello!
> 2 + 3
5
> 
```

Press Ctrl+C to exit.

---

## Basic Syntax

### Comments

```tombo
# This is a comment
println("This runs")  # Inline comment

/* Multi-line comment
   spans multiple lines
   useful for documentation */
println("This also runs")
```

### Printing Output

```tombo
# Print with newline
println("Hello, World!")

# Print without newline
print("Hello ")
print("World")

# Print multiple values
println("Value: " + str(42))
```

### Variables

```tombo
# Declare and assign
let x = 42
let name = "Alice"
let pi = 3.14159

# Declare without assignment (must assign later)
let y: Int
y = 100

# Mutable variable
mut counter = 0
counter = 1  # Allowed
counter = 2  # Allowed

# Using variables
println("Name: " + name)
println("Value: " + str(x))
```

### Data Types

```tombo
# Integers
let age = 25
let negative = -10
let big = 1000000

# Floats
let temperature = 98.6
let pi = 3.14159

# Strings
let greeting = "Hello"
let message = 'Single quotes work too'
let multiline = "Line 1\nLine 2"

# Booleans
let is_active = true
let is_complete = false

# Lists
let numbers = [1, 2, 3, 4, 5]
let mixed = [1, "two", 3.0, true]
let empty = []

# Dictionaries
let person = {"name": "Alice", "age": 30, "city": "NYC"}
let empty_dict = {}

# Sets
let unique = {1, 2, 3}  # Automatically removes duplicates

# Tuples
let coordinates = (10, 20)
let mixed_tuple = (1, "hello", true)

# Nil (null/none)
let nothing = nil
```

---

## Working with Data

### Strings

```tombo
use string

let text = "Hello, World!"

# Length
let len = length(text)  # 13

# Case conversion
let upper = upper(text)      # "HELLO, WORLD!"
let lower = lower(text)      # "hello, world!"
let title = title(text)      # "Hello, World!"
let cap = capitalize(text)   # "Hello, world!"

# Trimming
let padded = "  hello  "
let trimmed = strip(padded)  # "hello"

# Splitting and joining
let words = split(text, ", ")  # ["Hello", "World!"]
let rejoined = join(words, " - ")  # "Hello - World!"

# Searching
let index = find(text, "World")  # 7
let starts = startswith(text, "Hello")  # true
let ends = endswith(text, "!")  # true

# Replacing
let updated = replace(text, "World", "Tombo")  # "Hello, Tombo!"

# Reversing
let reversed = reverse(text)  # "!dlroW ,olleH"
```

### Lists

```tombo
use collections

let numbers = [1, 2, 3, 4, 5]

# Add items
append(numbers, 6)           # [1, 2, 3, 4, 5, 6]
insert(numbers, 0, 0)        # [0, 1, 2, 3, 4, 5, 6]
extend(numbers, [7, 8, 9])   # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Remove items
remove(numbers, 5)           # Removes value 5
pop(numbers)                 # Removes last item
clear(numbers)               # Empties list

# Get information
let count = count(numbers, 3)  # How many 3's?
let idx = index(numbers, 5)    # Index of value 5
let is_in = 3 in numbers       # true

# Access elements
let first = numbers[0]         # First element
let last = numbers[-1]         # Last element
let slice = numbers[1:3]       # Elements at index 1 and 2

# Iterate
for num in numbers
    println(num)
```

### Dictionaries

```tombo
use collections

let person = {
    "name": "Alice",
    "age": 30,
    "city": "NYC",
    "hobbies": ["reading", "gaming"]
}

# Get values
let name = person["name"]           # "Alice"
let age = get(person, "age")        # 30
let hobby = get(person, "hobbies")  # ["reading", "gaming"]

# Set values
person["age"] = 31
person["email"] = "alice@example.com"

# Check keys
let has_name = "name" in person     # true
let keys = keys(person)             # ["name", "age", "city", "hobbies", "email"]
let values = values(person)         # ["Alice", 31, "NYC", ["reading", "gaming"], "alice@example.com"]

# Get all items
let items = items(person)           # [["name", "Alice"], ["age", 31], ...]

# Remove items
del person["email"]
clear(person)  # Empty dictionary

# Iterate
for key, value in person
    println(key + ": " + str(value))
```

---

## Control Flow

### If/Else Statements

```tombo
let age = 25

# Basic if
if age >= 18
    println("You are an adult")

# If/else
if age < 13
    println("Child")
else
    println("Not a child")

# If/elif/else
if age < 13
    println("Child")
elif age < 18
    println("Teenager")
elif age < 65
    println("Adult")
else
    println("Senior")

# Single-line if (expression form)
let status = if age >= 18 then "adult" else "minor"
println(status)  # "adult"
```

### Loops

```tombo
# While loop
let count = 0
while count < 5
    println(count)
    count = count + 1

# For loop with range
for i in range(0, 5)
    println(i)  # 0, 1, 2, 3, 4

# For loop with step
for i in range(0, 10, 2)
    println(i)  # 0, 2, 4, 6, 8

# For loop over list
let fruits = ["apple", "banana", "cherry"]
for fruit in fruits
    println(fruit)

# For loop over dictionary
let scores = {"alice": 95, "bob": 87, "charlie": 92}
for name, score in scores
    println(name + ": " + str(score))

# Break and continue
for i in range(0, 10)
    if i == 5
        break
    if i % 2 == 0
        continue  # Skip even numbers
    println(i)
```

### Match Expressions

```tombo
let day = 3

let day_name = match day
    case 1:
        "Monday"
    case 2:
        "Tuesday"
    case 3:
        "Wednesday"
    case _:  # Default case
        "Unknown"

println(day_name)  # "Wednesday"
```

---

## Functions

### Basic Functions

```tombo
# Function with parameters and return type
fn add(a: Int, b: Int) -> Int
    return a + b

# Call the function
let result = add(3, 4)  # 7

# Implicit return (no 'return' keyword needed)
fn multiply(x: Int, y: Int) -> Int
    x * y

result = multiply(3, 4)  # 12

# Function without parameters
fn get_greeting() -> String
    "Hello, Tombo!"

println(get_greeting())

# Function with no return value
fn say_goodbye(name: String)
    println("Goodbye, " + name)

say_goodbye("Alice")  # Prints: Goodbye, Alice
```

### Default Parameters

```tombo
fn greet(name: String, greeting: String = "Hello") -> String
    greeting + ", " + name

println(greet("Alice"))              # "Hello, Alice"
println(greet("Bob", "Hi"))          # "Hi, Bob"
```

### Variable Arguments

```tombo
fn sum_all(numbers...) -> Int
    let total = 0
    for num in numbers
        total = total + num
    return total

result = sum_all(1, 2, 3, 4, 5)  # 15
```

### Lambda Functions

```tombo
# Anonymous function stored in variable
let square = fn(x) -> x * x
println(square(5))  # 25

# Used with higher-order functions
use iter

let numbers = [1, 2, 3, 4, 5]
let squared = map(numbers, fn(x) -> x * x)
println(squared)  # [1, 4, 9, 16, 25]

let evens = filter(numbers, fn(x) -> x % 2 == 0)
println(evens)  # [2, 4]
```

### Recursive Functions

```tombo
fn factorial(n: Int) -> Int
    if n <= 1
        return 1
    else
        return n * factorial(n - 1)

println(factorial(5))  # 120

fn fibonacci(n: Int) -> Int
    if n <= 1
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

println(fibonacci(7))  # 13
```

---

## Using Libraries

### Loading Libraries

```tombo
# Load specific library
use math

# Now you can use math functions
let root = sqrt(16)  # 4.0
let value = sin(pi / 2)  # 1.0

# Load multiple libraries
use string
use collections

text = upper("hello")  # "HELLO"
numbers = [1, 2, 3]
append(numbers, 4)     # [1, 2, 3, 4]
```

### Core Libraries

```tombo
use core           # Type system
use math           # Math operations
use string         # String manipulation
use collections    # List/dict/set operations
use io             # Input/output
use time           # Time operations
use regex          # Regular expressions
use json           # JSON parsing
use crypto         # Cryptography
use os             # OS operations
```

### Domain Libraries

```tombo
use web            # Web development
use database       # Databases
use ml             # Machine learning
use vision         # Computer vision
use sensors        # Sensor integration
use env_sensors    # Environmental monitoring
use bio_sensors    # Health/biometric data
use game           # Game development
use audio          # Audio processing
use robotics       # Robotics
# ... and many more (39 total)
```

---

## Common Patterns

### Working with File I/O

```tombo
use io

# Write to file
write_file(path: "output.txt", content: "Hello, World!")

# Read from file
let content = read_file(path: "output.txt")
println(content)

# Append to file
append_file(path: "output.txt", content: "\nNew line")

# Check if file exists
let exists = file_exists(path: "output.txt")

# List files in directory
let files = list_directory(path: ".")
```

### Error Handling

```tombo
try
    # Risky operation
    let data = read_file("missing.txt")
    let result = data / 0
catch error
    println("Error occurred: " + str(error))
finally
    println("Cleanup done")
```

### Processing Collections

```tombo
use iter
use collections

let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Map - transform each element
let squared = map(numbers, fn(x) -> x * x)
println(squared)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# Filter - keep elements matching condition
let evens = filter(numbers, fn(x) -> x % 2 == 0)
println(evens)  # [2, 4, 6, 8, 10]

# Reduce - combine elements into single value
let sum = reduce(numbers, 0, fn(acc, x) -> acc + x)
println(sum)  # 55

# Zip - combine lists
let list1 = [1, 2, 3]
let list2 = ["a", "b", "c"]
let zipped = zip(list1, list2)
println(zipped)  # [[1, "a"], [2, "b"], [3, "c"]]

# Enumerate - get index and value
let indexed = enumerate(["apple", "banana", "cherry"])
for idx, fruit in indexed
    println(str(idx) + ": " + fruit)
```

### JSON Operations

```tombo
use json

# Parse JSON string
let json_string = '{"name": "Alice", "age": 30}'
let data = parse_json(json_string)
println(data["name"])  # "Alice"

# Convert to JSON string
let person = {"name": "Bob", "age": 25}
let json_output = to_json(person)
println(json_output)  # '{"name": "Bob", "age": 25}'

# Pretty print JSON
pretty_print(person)
```

---

## Troubleshooting

### Common Errors

#### Error: `variable not found`

```tombo
# WRONG
println(name)  # Error: 'name' not defined

# RIGHT
let name = "Alice"
println(name)
```

#### Error: `type mismatch`

```tombo
# WRONG
let x: Int = "hello"  # Error: can't assign string to int

# RIGHT
let x: Int = 42
let y: String = "hello"
```

#### Error: `unexpected indentation`

```tombo
# WRONG
let x = 5
  let y = 10  # Error: unexpected indentation

# RIGHT
let x = 5
let y = 10

# Indentation needed for blocks:
if x > 0
    println("positive")  # Indented correctly
```

#### Error: `function not found`

```tombo
# WRONG
let upper_text = upper("hello")  # Error: function not found

# RIGHT
use string
let upper_text = upper("hello")  # "HELLO"
```

### Tips for Success

1. **Use type annotations** - Makes code clearer and catches errors early
2. **Read error messages carefully** - They tell you exactly what's wrong
3. **Check indentation** - Python-style indentation matters
4. **Test incrementally** - Build and test small pieces before combining
5. **Use the REPL** - Test functions interactively
6. **Read documentation** - Check the Language Reference for library details

---

## Next Steps

1. **Review the Language Reference** - Full syntax and library documentation
2. **Explore Phase 4 Libraries** - Vision, sensors, environment, biometrics
3. **Check Examples** - See complete programs in the examples directory
4. **Join Community** - Share your Tombo programs and learn from others

---

## Quick Cheat Sheet

```tombo
# Variables
let x = 10
mut y = 20

# Data types
[1, 2, 3]              # List
{"key": "value"}       # Dictionary
{1, 2, 3}              # Set
(1, 2, 3)              # Tuple

# Control flow
if condition
    # do something
for item in list
    # loop over items
while condition
    # loop

# Functions
fn name(param: Type) -> Type
    return param

# Libraries
use library_name
function_name(arg)
```

---

**Happy coding with Tombo!** 🚀
