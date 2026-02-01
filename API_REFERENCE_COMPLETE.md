# TOMBO Language - Complete API Reference

## Table of Contents
1. [Core Language](#core-language)
2. [Built-in Functions](#built-in-functions)
3. [I/O Domain](#io-domain)
4. [Web Domain](#web-domain)
5. [Database Domain](#database-domain)
6. [ML Domain](#ml-domain)
7. [Math Domain](#math-domain)
8. [String Domain](#string-domain)
9. [Utility Domains](#utility-domains)

---

## Core Language

### Variables & Assignment

```tombo
let x = value       # Declare variable
change x to value   # Modify variable
```

### Data Types

- **Integer**: `42`, `-10`, `0`
- **Float**: `3.14`, `-2.5`, `1e-6`
- **String**: `"hello"`, `'world'`, multi-line with proper indentation
- **Boolean**: `true`, `false`
- **List**: `[1, 2, 3]`, `[1, "two", 3.0]`
- **Dict**: `{"key": value, "name": "value"}`
- **None**: `None`

### Control Flow

```tombo
# If statement
if condition
    # statements
elif other_condition
    # statements
else
    # statements
end

# While loop
while condition
    # statements
    break           # exit loop
    continue        # skip to next iteration
end

# For loop
for variable in iterable
    # statements
end

# Match statement
match value
    when pattern1
        # statements
    when pattern2
        # statements
end
```

### Functions

```tombo
def function_name(param1, param2)
    # function body
    return value
end

# Call function
result = function_name(arg1, arg2)
```

### Operators

**Arithmetic**: `+`, `-`, `*`, `/`, `//`, `%`, `**`

**Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`

**Logical**: `and`, `or`, `not`

**Bitwise**: `&`, `|`, `^`, `~`, `<<`, `>>`

**Assignment**: `=`, `+=`, `-=`, `*=`, `/=`

---

## Built-in Functions

### Type Functions

- `type(x)` - Get type of value
- `len(x)` - Get length of sequence/collection
- `isinstance(x, type)` - Check type
- `int(x)` - Convert to integer
- `float(x)` - Convert to float
- `str(x)` - Convert to string
- `bool(x)` - Convert to boolean
- `list(x)` - Convert to list
- `dict(pairs)` - Create dictionary
- `range(start, stop, step)` - Create range

### Sequence Functions

- `append(list, item)` - Add item to list
- `extend(list, items)` - Extend list with items
- `insert(list, index, item)` - Insert at position
- `remove(list, item)` - Remove first occurrence
- `pop(list, index)` - Remove and return item
- `clear(list)` - Remove all items
- `index(list, item)` - Find index of item
- `count(list, item)` - Count occurrences
- `reverse(list)` - Reverse list in-place
- `sort(list)` - Sort list in-place

### Output Functions

- `print(*items)` - Print without newline
- `println(*items)` - Print with newline
- `printf(format, *args)` - Formatted print

### Input Functions

- `input(prompt)` - Read line from user
- `ask(prompt)` - Read line (alias for input)
- `input_number(prompt)` - Read number from user
- `input_bool(prompt)` - Read boolean from user

---

## I/O Domain

### File Operations

```tombo
# Write file
write_file(path, content)
write_file_bytes(path, bytes)

# Read file
let content = read_file(path)
let bytes = read_file_bytes(path)

# Append to file
append_file(path, content)

# Check if file exists
if file_exists(path)
    # ...
end

# Delete file
delete_file(path)

# File size
let size = file_size(path)

# List directory
let files = list_dir(path)

# Create directory
create_dir(path)

# Remove directory
remove_dir(path)

# Copy file
copy_file(src, dest)

# Move/rename file
move_file(src, dest)
rename_file(old_name, new_name)

# Get absolute path
let abs = absolute_path(relative_path)

# Get file extension
let ext = get_extension(path)

# Join paths
let path = join_path(dir, file)
```

### Path Operations

```tombo
# Get current working directory
let cwd = get_cwd()

# Change directory
change_dir(path)

# Get home directory
let home = get_home_dir()

# Path exists
if path_exists(path)
    # ...
end

# Is file
if is_file(path)
    # ...
end

# Is directory
if is_dir(path)
    # ...
end

# Is link
if is_link(path)
    # ...
end
```

---

## Web Domain

### HTTP Client

```tombo
# Basic requests
let resp = get(url)
let resp = post(url, body)
let resp = put(url, body)
let resp = delete(url)
let resp = patch(url, body)
let resp = head(url)
let resp = options(url)

# JSON requests
let resp = post_json(url, data)
let resp = put_json(url, data)

# Response methods
resp.status           # HTTP status code
resp.headers          # Response headers dict
resp.body             # Raw body
resp.text()           # Body as text
resp.json()           # Parse body as JSON

# URL utilities
let url = build_url(base, path, params)
let parsed = parse_url(url)
let encoded = url_encode(data)
let decoded = url_decode(query_string)
```

### Request Configuration

```tombo
# Headers
let headers = {
    "User-Agent": "TOMBO/1.0",
    "Authorization": "Bearer token"
}
let resp = get(url, headers)

# Timeout
let resp = get(url, headers, timeout)
```

---

## Database Domain

### SQLite Operations

```tombo
# Open database
let db = create_file_db("data.db")
let db = create_in_memory_db()

# Close database
close_database(db)

# Create table
create_table_from_schema(db, "users", {
    "id": "INTEGER PRIMARY KEY",
    "name": "TEXT NOT NULL",
    "email": "TEXT UNIQUE",
    "age": "INTEGER"
})

# Insert data
let id = insert_row(db, "users", {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
})

# Insert multiple
let ids = insert_many(db, "users", [
    {"name": "Bob", "email": "bob@example.com", "age": 25},
    {"name": "Carol", "email": "carol@example.com", "age": 35}
])

# Query
let rows = execute_query(db, "SELECT * FROM users")
let row = execute_single(db, "SELECT * FROM users WHERE id = 1")

# Update
let affected = update_rows(db, "users", {"age": 31}, "id = 1")

# Delete
let deleted = delete_rows(db, "users", "age > 50")

# Count
let count = execute_query(db, "SELECT COUNT(*) as count FROM users")[0]["count"]

# Check table exists
if db.table_exists("users")
    # ...
end

# List tables
let tables = db.list_tables()
```

### Query Builder

```tombo
let qb = query_builder("users")
let sql = qb.select("name", "email")
    .where("age > 18")
    .where("age < 65")
    .order_by("name", "ASC")
    .limit(10)
    .build()

let results = execute_query(db, sql)
```

---

## ML Domain

### Datasets

```tombo
# Create dataset
let features = [[1, 2], [2, 4], [3, 6], [4, 8]]
let labels = [0, 1, 1, 1]
let dataset = create_dataset(features, labels)

# Split dataset
let train, test = dataset.split(0.2)  # 80% train, 20% test

# Normalize
dataset.normalize()

# Shuffle
dataset.shuffle()

# Access data
let features = train.features
let labels = train.labels
```

### Models

#### Linear Regression

```tombo
let model = linear_regression(learning_rate=0.01, iterations=1000)
model.fit(X_train, y_train)

let predictions = model.predict(X_test)
let r2_score = model.score(X_test, y_test)
```

#### Logistic Regression

```tombo
let model = logistic_regression(learning_rate=0.01, iterations=1000)
model.fit(X_train, y_train)

let predictions = model.predict(X_test)
let probabilities = model.predict_proba(X_test)
let acc = model.accuracy(X_test, y_test)
```

#### K-Nearest Neighbors

```tombo
let model = knn(k=3)
model.fit(X_train, y_train)

let predictions = model.predict(X_test)
let acc = model.accuracy(X_test, y_test)
```

### Utilities

```tombo
# Train/test split
let X_train, X_test, y_train, y_test = train_test_split(X, y, 0.2)

# Normalize features
let X_normalized = normalize_features(X)

# Metrics
let mse = mean_squared_error(y_true, y_pred)
let acc = accuracy_score(y_true, y_pred)
```

---

## Math Domain

### Constants

- `PI` - π (3.14159...)
- `E` - e (2.71828...)
- `TAU` - 2π
- `PHI` - Golden ratio
- `INF` - Positive infinity
- `NAN` - Not a number

### Basic Functions

```tombo
abs(x)              # Absolute value
min(a, b, ...)      # Minimum
max(a, b, ...)      # Maximum
ceil(x)             # Round up
floor(x)            # Round down
round(x, digits)    # Round to n decimal places
sqrt(x)             # Square root
cbrt(x)             # Cube root
pow(x, y)           # x^y
exp(x)              # e^x
log(x)              # Natural logarithm
log10(x)            # Base-10 logarithm
log2(x)             # Base-2 logarithm
sign(x)             # -1, 0, or 1
clamp(x, min, max)  # Clamp between bounds
```

### Trigonometry

```tombo
sin(x)              # Sine (radians)
cos(x)              # Cosine
tan(x)              # Tangent
asin(x)             # Inverse sine
acos(x)             # Inverse cosine
atan(x)             # Inverse tangent
atan2(y, x)         # Two-argument arctangent
sinh(x)             # Hyperbolic sine
cosh(x)             # Hyperbolic cosine
tanh(x)             # Hyperbolic tangent
degrees(x)          # Radians to degrees
radians(x)          # Degrees to radians
```

### Special Functions

```tombo
factorial(n)        # n!
gcd(a, b)          # Greatest common divisor
lcm(a, b)          # Least common multiple
is_prime(n)        # Check if prime
is_nan(x)          # Check if NaN
is_inf(x)          # Check if infinity
```

### Statistics

```tombo
mean(values)        # Arithmetic mean
median(values)      # Median
mode(values)        # Most frequent value
stddev(values)      # Standard deviation
variance(values)    # Variance
sum(values)         # Sum
product(values)     # Product
percentile(values, p)  # p-th percentile
```

### Geometry

```tombo
distance(x1, y1, x2, y2)          # 2D distance
distance_3d(x1, y1, z1, x2, y2, z2)  # 3D distance
lerp(a, b, t)                      # Linear interpolation
```

---

## String Domain

### Case Operations

```tombo
upper(s)            # To uppercase
lower(s)            # To lowercase
title(s)            # Title case
capitalize(s)       # Capitalize first
swapcase(s)         # Swap case
```

### Trimming & Padding

```tombo
strip(s)            # Remove whitespace
lstrip(s)           # Left strip
rstrip(s)           # Right strip
center(s, width)    # Center in field
ljust(s, width)     # Left justify
rjust(s, width)     # Right justify
zfill(s, width)     # Zero pad
```

### Searching & Replacing

```tombo
contains(s, substr)         # Check contains
startswith(s, prefix)       # Check prefix
endswith(s, suffix)         # Check suffix
index_of(s, substr)         # Find index
rindex_of(s, substr)        # Find last index
count(s, substr)            # Count occurrences
replace(s, old, new)        # Replace all
```

### Splitting & Joining

```tombo
split(s, delim)             # Split by delimiter
join(sep, items)            # Join items
repeat(s, times)            # Repeat string
```

### Checking

```tombo
isdigit(s)          # All digits
isalpha(s)          # All alphabetic
isalnum(s)          # All alphanumeric
isspace(s)          # All whitespace
isupper(s)          # All uppercase
islower(s)          # All lowercase
```

### Regular Expressions

```tombo
regex_match(pattern, s)        # Match entire string
regex_search(pattern, s)       # Find first match
regex_findall(pattern, s)      # Find all matches
regex_split(pattern, s)        # Split by pattern
regex_replace(pattern, repl, s) # Replace by pattern
regex_extract_groups(pattern, s) # Extract groups
```

### Text Processing

```tombo
length(s)           # String length
reverse(s)          # Reverse string
word_count(s)       # Count words
char_frequency(s)   # Frequency of each char
truncate(s, len)    # Truncate with ellipsis
slugify(s)          # URL-safe slug
camel_to_snake(s)   # camelCase → snake_case
snake_to_camel(s)   # snake_case → camelCase
```

### String Similarity

```tombo
levenshtein_distance(s1, s2)   # Edit distance
string_similarity(s1, s2)       # Similarity 0-1
hamming_distance(s1, s2)       # Hamming distance
```

### Text Formatting

```tombo
format(template, args...)       # Format string
indent(text, prefix)            # Add indent
dedent(text)                    # Remove indent
wrap(text, width)               # Wrap to width
fill(text, width)               # Fill to width
```

---

## Utility Domains

### JSON

```tombo
json_encode(obj)        # Object to JSON string
json_decode(s)          # JSON string to object
```

### Time

```tombo
current_time()                  # Current timestamp
time_to_timestamp(y, m, d, h, min, s)  # Convert to timestamp
sleep(seconds)                  # Sleep
```

### Random

```tombo
random_int(min, max)    # Random integer
random_float()          # Random float [0, 1)
random_choice(list)     # Pick random item
shuffle(list)           # Shuffle list in-place
```

### Hashing

```tombo
md5(s)                  # MD5 hash
sha1(s)                 # SHA1 hash
sha256(s)               # SHA256 hash
```

### System

```tombo
get_cwd()               # Current working directory
change_dir(path)        # Change directory
environ()               # Environment variables
system(cmd)             # Execute system command
```

---

*For more information, see individual domain documentation.*
*Visit: https://tombo.example.com/docs*
