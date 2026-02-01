# TOMBO Language - Quick Start Examples

## Basic Syntax

```tombo
# Variables and basic operations
let x = 10
let y = 20
let name = "TOMBO"

println("Hello from " + name)

# Math operations
let sum = x + y
let product = x * y
println("Sum: " + sum)
```

## Control Flow

```tombo
# If/Elif/Else
let age = 25
if age < 18
    println("Minor")
elif age < 65
    println("Adult")
else
    println("Senior")
end

# While loop
let count = 0
while count < 5
    println(count)
    change count to count + 1
end

# For loop
for i in range(5)
    println(i)
end
```

## Functions

```tombo
# Define a function
def greet(name)
    println("Hello, " + name)
end

greet("World")

# Function with return value
def add(a, b)
    return a + b
end

let result = add(3, 4)
println(result)
```

## Working with Collections

```tombo
# Lists
let numbers = [1, 2, 3, 4, 5]
println(length(numbers))
println(numbers[0])

# Dictionaries
let person = {"name": "Alice", "age": 30}
println(person["name"])
```

## String Operations

```tombo
let text = "Hello World"
println(upper(text))
println(lower(text))
println(replace(text, "World", "TOMBO"))

# String splitting
let parts = split("a,b,c", ",")
println(parts)
```

## Using the Math Library

```tombo
println(sqrt(16))
println(pow(2, 8))
println(sin(PI / 2))
println(max(1, 2, 3, 4, 5))
println(min(1, 2, 3, 4, 5))
```

## File I/O

```tombo
# Write to file
write_file("output.txt", "Hello, File!")

# Read from file
let content = read_file("output.txt")
println(content)

# List directory
let files = list_dir(".")
println(files)
```

## Web Requests

```tombo
# Make GET request
let response = get("https://api.example.com/data")
println(response.status)
println(response.text())

# POST with JSON
let data = {"key": "value"}
let response = post_json("https://api.example.com/endpoint", data)
```

## Database Operations

```tombo
# Create and use database
let db = create_file_db("mydata.db")

# Create table
create_table_from_schema(db, "users", {
    "id": "INTEGER PRIMARY KEY",
    "name": "TEXT NOT NULL",
    "age": "INTEGER"
})

# Insert data
insert_row(db, "users", {"name": "Alice", "age": 30})

# Query data
let users = execute_query(db, "SELECT * FROM users")
println(users)

close_database(db)
```

## Machine Learning

```tombo
# Create and train a simple model
let dataset = create_dataset([[1, 2], [2, 4], [3, 6]], [0, 0, 1])
let train, test = dataset.split(0.2)

let model = logistic_regression(0.01, 100)
model.fit(train.features, train.labels)

# Make predictions
let predictions = model.predict(test.features)
let acc = model.accuracy(test.features, test.labels)
println("Accuracy: " + acc)
```

## JSON Operations

```tombo
let data = {"name": "Bob", "age": 25}

# Convert to JSON string
let json_str = json_encode(data)
println(json_str)

# Parse JSON
let parsed = json_decode('{"x": 1, "y": 2}')
println(parsed["x"])
```

## Time and Scheduling

```tombo
# Get current time
let now = current_time()
println(now)

# Sleep
sleep(1)
println("1 second later")

# Time operations
let timestamp = time_to_timestamp(2024, 2, 1, 12, 0, 0)
println(timestamp)
```

## Random Operations

```tombo
# Random number
let rand_int = random_int(1, 100)
println(rand_int)

# Random float
let rand_float = random_float()
println(rand_float)

# Shuffle list
let items = [1, 2, 3, 4, 5]
shuffle(items)
println(items)
```

## Error Handling

```tombo
try
    let x = 10 / 0
catch
    println("Division by zero!")
end
```

## Real-World Examples

### Web Scraper

```tombo
def fetch_data(url)
    let response = get(url)
    if response.status == 200
        return response.json()
    else
        return None
    end
end

let data = fetch_data("https://api.example.com/users")
for user in data
    println(user["name"])
end
```

### Data Processing

```tombo
let db = create_file_db("sales.db")

# Assuming sales table exists
let sales = execute_query(db, "SELECT * FROM sales")

# Calculate statistics
let total = 0
for sale in sales
    change total to total + sale["amount"]
end

let average = total / length(sales)
println("Total: " + total)
println("Average: " + average)

close_database(db)
```

### ML Classifier

```tombo
# Load training data
let features = [[5.1, 3.5, 1.4], [7.0, 3.2, 4.7], [6.3, 3.3, 6.0]]
let labels = [0, 1, 2]

# Create and train
let model = knn(3)
model.fit(features, labels)

# Make predictions
let predictions = model.predict([[5.5, 3.0, 1.5]])
println(predictions)
```

---

*For more examples, see the examples/ directory*
