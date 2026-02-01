# Phase 3 Libraries - Quick Start Guide

## Overview

Phase 3 adds 2 major professional-grade libraries with 140+ functions for testing and mobile development.

**Libraries Added:**
- **Testing Framework** (750+ lines) - Unit testing, fixtures, mocks
- **Mobile** (850+ lines) - UI, sensors, notifications, app lifecycle

---

## 1. Testing Framework Library

Professional unit testing framework with assertions, fixtures, and test runners.

### Basic Test Case

```tombo
use testing

let TestMath = TestCase("TestMath")

// Define test methods
let test_addition = fn() {
    let assert = Assertion()
    assert.assert_equal(2 + 2, 4)
}

let test_subtraction = fn() {
    let assert = Assertion()
    assert.assert_equal(5 - 3, 2)
}

// Create and run tests
let runner = TestRunner(1)  // verbosity = 1
let result = runner.run_tests(TestMath)

println(result.get_summary())
```

### Assertions

```tombo
use testing

let assert = Assertion()

// Equality
assert.assert_equal(5, 5)
assert.assert_not_equal(5, 3)

// Boolean
assert.assert_true(true)
assert.assert_false(false)

// None checking
assert.assert_is_none(nil)
assert.assert_is_not_none(5)

// Comparisons
assert.assert_greater(10, 5)
assert.assert_less(3, 5)
assert.assert_greater_equal(5, 5)
assert.assert_less_equal(3, 5)

// Container checks
assert.assert_in(2, [1, 2, 3])
assert.assert_not_in(4, [1, 2, 3])

// Floating point
assert.assert_almost_equal(3.14159, 3.14, 2)

// Type checking
assert.assert_is_instance([1, 2, 3], list)

// Collection equality
assert.assert_list_equal([1, 2, 3], [1, 2, 3])
assert.assert_dict_equal({"a": 1}, {"a": 1})

// Exception handling
let fn_that_fails = fn() { throw "error" }
assert.assert_raises(Exception, fn_that_fails)
```

### Test Fixtures

```tombo
use testing

let fixture = TestFixture("MyFixture")

// Setup before tests
fixture.setup()

// Store test data
fixture.set_data("users", ["Alice", "Bob", "Charlie"])
fixture.set_data("count", 42)

// Use in tests
let users = fixture.get_data("users")
let count = fixture.get_data("count")

// Cleanup after tests
fixture.teardown()
```

### Test Fixtures with Lifecycle

```tombo
use testing

let TestWithLifecycle = TestCase("TestWithLifecycle")

TestWithLifecycle.setUp = fn() {
    println("Setting up test")
    self.test_data = [1, 2, 3]
}

TestWithLifecycle.tearDown = fn() {
    println("Tearing down test")
    self.test_data = nil
}

let test_data_length = fn() {
    let assert = Assertion()
    assert.assert_equal(len(self.test_data), 3)
}
```

### Mock Objects

```tombo
use testing

let mock = MockObject()

// Call methods on mock
mock.send_email("user@example.com")
mock.send_email("admin@example.com")
mock.log_event("test_event")

// Verify calls
if mock.assert_called("send_email") {
    println("send_email was called")
}

if mock.assert_called_with("send_email", "user@example.com") {
    println("send_email called with correct args")
}

// Set return values
mock.set_return_value("get_user_id", 123)
let user_id = mock.get_user_id()
```

### Parameterized Tests

```tombo
use testing

let assert = Assertion()

let test_multiplication = fn(a, b, expected) {
    assert.assert_equal(a * b, expected)
}

let params = [
    (2, 3, 6),
    (4, 5, 20),
    (10, 10, 100)
]

let param_test = ParameterizedTest(test_multiplication, params)
let runner = TestRunner(0)
let result = param_test.run(runner)

println(result.get_summary())
```

### Test Suites

```tombo
use testing

let suite = TestSuite("FullTestSuite")

let test1 = TestCase("Test1")
let test2 = TestCase("Test2")

suite.add_test(test1)
suite.add_test(test2)

let runner = TestRunner(1)
let result = suite.run(runner)

println(result.get_summary())
println("Total tests: " + result.tests_run)
println("Passed: " + result.successes)
println("Failed: " + result.failures)
```

### Test Results

```tombo
use testing

let runner = TestRunner()
let result = runner.run_tests(my_test_case)

// Check result
if result.was_successful() {
    println("All tests passed!")
}

// Get statistics
println("Tests run: " + result.tests_run)
println("Successes: " + result.successes)
println("Failures: " + result.failures)
println("Errors: " + result.errors)
println("Skipped: " + result.skipped)

// Get detailed info
for detail in result.test_details {
    println(detail.name + ": " + detail.status)
    if detail.status == "FAIL" {
        println("  Message: " + detail.message)
    }
}
```

---

## 2. Mobile Library

Complete mobile app framework with UI, sensors, notifications, and app lifecycle.

### Creating a Mobile App

```tombo
use mobile

// Create app
let app = Application("MyApp")
app.version = "1.0.0"

// Create screens
let main_screen = app.create_screen("main")
let settings_screen = app.create_screen("settings")

// Start app
app.start()
```

### Building User Interfaces

```tombo
use mobile

let screen = Screen("MainScreen")

// Add widgets
let title = TextView("txt_title", "Welcome")
let input = EditText("edt_name", "Enter name...")
let submit = Button("btn_submit", "Submit")
let list = ListView("lst_items")

screen.add_widget(title)
screen.add_widget(input)
screen.add_widget(submit)
screen.add_widget(list)

// Configure widgets
title.set_position(0, 0)
title.set_size(100, 20)

input.set_position(0, 20)
input.set_size(100, 30)

submit.set_position(0, 50)
submit.set_size(100, 30)

// Widget events
submit.on_click(fn() {
    let name = input.get_text()
    println("Name: " + name)
})
```

### Button and Text Views

```tombo
use mobile

let button = Button("btn1", "Click Me")
let textview = TextView("txt1", "Hello World")

// Update text
button.set_text("Click Again")
textview.set_text("Updated text")
textview.append_text(" - More text")

// Text properties
textview.text_size = 16
textview.text_color = "BLUE"

// Button click
button.on_click(fn() {
    textview.set_text("Button was clicked!")
})

button.click()  // Simulate click
```

### Edit Text Input

```tombo
use mobile

let input = EditText("edt_password", "Enter password...")

// Get and set text
input.set_text("initial value")
let current = input.get_text()

// Clear
input.clear()

// Input type
input.input_type = "password"
input.input_type = "number"
input.input_type = "email"
```

### List Views

```tombo
use mobile

let list = ListView("lst_users")

// Add items
list.add_item("Alice")
list.add_item("Bob")
list.add_item("Charlie")

// Select item
list.select_item(0)
let selected = list.get_selected_item()

// Get specific item
let item = list.get_item(1)

// Modify list
list.remove_item(2)
list.clear()
```

### Sensors

```tombo
use mobile

let app = Application("SensorApp")

// Accelerometer
let accel = app.accelerometer
accel.enable()
accel.set_acceleration(1.0, 2.0, 3.0)
let x, y, z = accel.get_acceleration()

// Gyroscope
let gyro = app.gyroscope
gyro.enable()
gyro.set_rotation(10.0, 20.0, 30.0)
let rx, ry, rz = gyro.get_rotation()

// GPS
let gps = app.gps
gps.set_location(37.7749, -122.4194)
let lat, lon = gps.get_location()

// Distance calculation
let distance = gps.distance_to(37.8044, -122.2712)
println("Distance: " + distance + " km")

// Sensor listeners
accel.add_listener(fn(value) {
    println("Accel: " + value)
})
```

### Notifications

```tombo
use mobile

let app = Application("NotifyApp")

// Send notification
app.send_notification("Hello", "This is a notification")

// Create notification with actions
let notif = Notification("Important", "Read me!")
notif.set_priority(2)
notif.add_action("reply")
notif.add_action("delete")

// Send
app.notification_manager.send_notification(notif)

// Listen for notifications
app.notification_manager.add_listener(fn(notif) {
    println("Received: " + notif.title)
})

// Mark as read
notif.mark_read()

// Get all notifications
let all_notifs = app.notification_manager.get_notifications()
```

### Persistent Storage

```tombo
use mobile

let app = Application("StorageApp")
let prefs = app.preferences

// Store values
prefs.set("username", "john")
prefs.set("user_id", 123)
prefs.set("premium", true)

// Retrieve values
let username = prefs.get_string("username")
let user_id = prefs.get_int("user_id")
let is_premium = prefs.get_boolean("premium")

// Defaults
let status = prefs.get("status", "inactive")

// Remove
prefs.remove("username")

// Clear all
prefs.clear()
```

### Screen Navigation

```tombo
use mobile

let app = Application("NavApp")

let home = app.create_screen("home")
let profile = app.create_screen("profile")
let settings = app.create_screen("settings")

// Navigate with Intent
let intent = Intent("profile")
intent.put_extra("user_id", 123)
intent.put_extra("show_details", true)

let am = ActivityManager(app)
am.start_activity(intent)

// Current screen
let current = app.current_screen

// Go back
am.go_back()
```

### Complete App Example

```tombo
use mobile

// Create app
let app = Application("TodoApp")

// Create screens
let main = app.create_screen("main")
let add_task = app.create_screen("add_task")

// Build main screen
let title = TextView("title", "My Todos")
let list = ListView("todos")
let add_btn = Button("btn_add", "Add Task")

main.add_widget(title)
main.add_widget(list)
main.add_widget(add_btn)

// Add sample data
list.add_item("Buy groceries")
list.add_item("Finish project")
list.add_item("Call mom")

// Add task button handler
add_btn.on_click(fn() {
    let intent = Intent("add_task")
    let am = ActivityManager(app)
    am.start_activity(intent)
})

// Build add task screen
let input = EditText("task_input", "Enter task...")
let save_btn = Button("btn_save", "Save")

add_task.add_widget(input)
add_task.add_widget(save_btn)

// Save button handler
save_btn.on_click(fn() {
    let task = input.get_text()
    if task != "" {
        list.add_item(task)
        let am = ActivityManager(app)
        am.go_back()
    }
})

// Store preferences
app.preferences.set("last_activity", "main")

// Start app
app.start()
app.set_screen("main")
```

---

## Module Summary

| Library | Size | Functions | Use Case |
|---------|------|-----------|----------|
| Testing Framework | 750 lines | 45+ | Unit testing, assertions, mocks |
| Mobile | 850 lines | 95+ | Mobile apps, UI, sensors |

**Total Phase 3:** 1,600 lines, 140+ functions

---

## Status

✅ **PHASE 3 COMPLETE**
- All 2 libraries implemented
- All functions tested
- Complete documentation provided
- Ready for production use

See `PHASE3_STATUS.txt` for full delivery details.
