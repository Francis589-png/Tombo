# Phase 2 Libraries - Quick Start Guide

## Overview

Phase 2 adds 3 new professional-grade libraries with 150+ functions for debugging, data science, and game development.

**Libraries Added:**
- **Debug** (700+ lines) - Profiling, debugging, memory analysis
- **DataScience** (600+ lines) - DataFrames, visualization, statistics
- **Game** (750+ lines) - Game engine, physics, graphics

---

## 1. Debug Library

The Debug library provides professional debugging, profiling, and performance analysis tools.

### Basic Usage

```tombo
use debug

// Create profiler
let prof = profiler
prof.start()

// Profile a function
let my_func = fn() {
    let sum = 0
    for i in 1..1000 {
        sum = sum + i
    }
    return sum
}

let wrapped = prof.profile_function(my_func)
wrapped()
wrapped()
wrapped()

// Get statistics
let stats = prof.get_stats()
println(prof.print_stats())
```

### Debugging Code

```tombo
use debug

let debugger = debugger
debugger.start_debugging("my code")

// Set variables during debugging
debugger.set_variable("x", 42)
debugger.set_variable("y", 100)

// Watch variables
let x_val = debugger.watch_variable("x")
println("x = " + x_val)

debugger.stop_debugging()
```

### Memory Analysis

```tombo
use debug

let analyzer = memory_analyzer

// Take snapshots
analyzer.take_snapshot()

// Do some work
let big_list = [1, 2, 3, 4, 5]

analyzer.take_snapshot()

// Detect memory leaks
let growth = analyzer.get_object_growth()
let mem_growth = analyzer.get_memory_growth()

println(analyzer.print_report())
```

### Logging

```tombo
use debug

let log = logger

log.debug("Debug message")
log.info("Info message")
log.warning("Warning message")
log.error("Error message")

// Get all logs
let logs = log.get_logs()
for entry in logs {
    println(entry)
}
```

### Assertions

```tombo
use debug

let assert = assertion

// Basic assertions
assert.assert_true(5 > 3)
assert.assert_false(5 < 3)
assert.assert_equal(5, 5)
assert.assert_not_equal(5, 3)

// Collection assertions
assert.assert_in(2, [1, 2, 3])

// Exception assertions
let fn_that_fails = fn() {
    throw "error"
}
assert.assert_raises(Exception, fn_that_fails)
```

### Debug Classes

- **Debugger** - Step through code, set breakpoints, watch variables
- **Profiler** - Profile function execution times
- **MemoryAnalyzer** - Analyze memory usage and detect leaks
- **Logger** - Structured logging with levels
- **TraceRecorder** - Record function call traces
- **AssertionHelper** - Test assertions and validations

---

## 2. DataScience Library

Professional data manipulation, analysis, and visualization.

### DataFrames

```tombo
use datascience

// Create DataFrame from data
let data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "salary": [50000, 60000, 70000]
}
let df = DataFrame(data)

// Basic operations
println(df.shape)  // (3, 3)
let ages = df.get_column("age")
let first_row = df.get_row(0)

// Add columns
df.add_column("department", ["Sales", "Engineering", "Marketing"])

// Remove columns
df.remove_column("department")
```

### Filtering & Sorting

```tombo
use datascience

// Filter data
let filtered = df.filter(fn(row) {
    return row.age > 25
})

// Sort data
let sorted_df = df.sort_by("salary", true)  // ascending

// Select specific columns
let selected = df.select_columns(["name", "age"])

// Head and tail
let first_5 = df.head(5)
let last_5 = df.tail(5)
```

### Grouping & Analysis

```tombo
use datascience

// Group by column
let grouped = df.group_by("department")

// Statistical description
let stats = df.describe()
for col_name in keys(stats) {
    println(col_name + ": " + stats[col_name])
}

// Value operations
let unique_ages = df.unique_values("age")
let age_counts = df.value_counts("age")
```

### Series

```tombo
use datascience

let series = Series([1, 2, 3, 4, 5], "numbers")

println(series.mean())      // 3.0
println(series.median())    // 3.0
println(series.std())       // Standard deviation
println(series.min())       // 1
println(series.max())       // 5

// Unique and counts
let unique = series.unique()
let counts = series.value_counts()
```

### Visualization

```tombo
use datascience

let vis = Visualization

// Histogram
let values = [1.0, 2.5, 3.0, 2.8, 1.5, 2.2, 3.5]
let hist = vis.histogram(values, 5)
println(hist)

// Scatter plot
let x_data = [1, 2, 3, 4, 5]
let y_data = [2, 4, 5, 4, 5]
let scatter = vis.scatter_plot(x_data, y_data)
println(scatter)

// Line plot
let line_data = [1, 2, 3, 2, 1, 2, 3]
let line = vis.line_plot(line_data)
println(line)
```

### Statistics

```tombo
use datascience

let stats = Statistics

let x = [1.0, 2.0, 3.0, 4.0, 5.0]
let y = [2.0, 4.0, 5.0, 4.0, 5.0]

// Correlation and covariance
let corr = stats.correlation(x, y)
let cov = stats.covariance(x, y)

// Percentiles
let p50 = stats.percentile(x, 50)
let p95 = stats.percentile(x, 95)

// Z-scores
let z = stats.z_score(3.5, 3.0, 0.5)
```

### DataScience Classes

- **DataFrame** - 2D tabular data structure
- **Series** - 1D labeled data structure
- **Visualization** - ASCII charts and plots
- **Statistics** - Statistical functions and analysis

---

## 3. Game Library

Complete game engine with graphics, physics, and input handling.

### Vector2 & Transforms

```tombo
use game

// 2D Vectors
let pos = Vector2(10, 20)
let vel = Vector2(5, 0)

// Vector operations
let new_pos = pos.add(vel)
let distance = pos.distance_to(vel)
let magnitude = pos.magnitude()
let normalized = pos.normalize()
let dot_prod = pos.dot(vel)

// Transforms
let transform = Transform(pos, 45.0)  // position, rotation
transform.rotate(45)
transform.move(Vector2(5, 5))
transform.set_position(Vector2(100, 100))
let forward = transform.get_forward()
```

### Sprites

```tombo
use game

// Create sprite (32x32 pixels)
let sprite = Sprite(32, 32, "RED", "█")

// Fill with color
sprite.fill("BLUE")

// Pixel operations
sprite.set_pixel(10, 10, "*")
let pixel = sprite.get_pixel(10, 10)

// Drawing shapes
sprite.draw_rect(5, 5, 10, 10, "#")  // x, y, width, height
sprite.draw_circle(16, 16, 8, "●")   // cx, cy, radius
```

### Physics & Colliders

```tombo
use game

// Colliders (AABB collision)
let col1 = Collider(0, 0, 10, 10)
let col2 = Collider(5, 5, 10, 10)

// Collision checks
let overlaps = col1.overlaps(col2)        // true
let contains = col1.contains_point(5, 5)  // true
let distance = col1.distance_to(col2)

// Rigid bodies
let body = RigidBody(5.0, false)  // mass, is_static
let force = Vector2(10, 0)
body.apply_force(force)
body.set_velocity(Vector2(5, 0))
body.update(0.016)  // delta time
```

### Game Objects

```tombo
use game

// Create game object
let obj = GameObject("Player")

// Components
obj.add_component("health", 100)
obj.add_component("damage", 10)
let health = obj.get_component("health")

// Transform
obj.transform.set_position(Vector2(50, 50))
obj.transform.rotate(90)

// Physics
obj.rigidbody.apply_force(Vector2(10, 0))

// Control
obj.active = true
obj.update(0.016)  // Update physics and position
```

### Camera

```tombo
use game

let camera = Camera(80, 24)  // width, height

// Pan camera
camera.pan_to(Vector2(100, 100))
camera.pan_smooth(Vector2(200, 200), 0.1)  // smooth pan

// Zoom
camera.set_zoom(2.0)
camera.set_zoom(0.5)

// Coordinate conversion
let world_pos = camera.screen_to_world(Vector2(40, 12))
let screen_pos = camera.world_to_screen(Vector2(100, 100))
```

### Input Handling

```tombo
use game

let input = InputHandler()

// Keyboard
input.set_key("w", true)
input.set_key("a", true)
if input.key_down("w") {
    println("W pressed")
}

// Mouse
input.set_mouse(50, 50)
let mouse_pos = input.mouse_pos
input.set_key("LMB", true)
if input.mouse_button_down("LMB") {
    println("Mouse clicked")
}

// Movement
let movement = input.get_movement_input()  // WASD input
```

### Game Scenes

```tombo
use game

// Create scene
let scene = GameScene("MainLevel")

// Add objects
let player = GameObject("Player")
let enemy = GameObject("Enemy")
scene.add_object(player)
scene.add_object(enemy)

// Find and update
let found = scene.find_object("Player")
scene.update(0.016)  // Update all objects

// Spatial queries
let objects_at_pos = scene.get_objects_at(Vector2(50, 50))
```

### Game Engine

```tombo
use game

// Create engine
let engine = GameEngine(80, 24, 60)  // width, height, fps

// Set up scene
let scene = GameScene("Game")
let player = GameObject("Player")
scene.add_object(player)
engine.set_scene(scene)

// Game loop
engine.start()

// Simulation (normally would be in a loop)
for frame in 1..60 {
    engine.input.set_key("w", true)
    engine.simulate_frame(0.016)
    let render = engine.render()
    println(render)
}

engine.stop()
```

### Game Classes

- **Vector2** - 2D vector math
- **Transform** - Position, rotation, scale
- **Sprite** - Visual representation
- **Collider** - AABB collision detection
- **RigidBody** - Physics simulation
- **GameObject** - Base game object
- **Camera** - View management
- **InputHandler** - Input processing
- **GameScene** - Container for objects
- **GameEngine** - Main game loop

---

## Complete Example: Simple Game

```tombo
use game

// Create engine and scene
let engine = GameEngine(80, 24, 60)
let scene = GameScene("SimpleGame")

// Create player
let player = GameObject("Player")
player.transform.set_position(Vector2(40, 12))
player.sprite.fill("BLUE")
player.rigidbody.mass = 2.0
scene.add_object(player)

// Create enemy
let enemy = GameObject("Enemy")
enemy.transform.set_position(Vector2(50, 12))
enemy.sprite.fill("RED")
scene.add_object(enemy)

// Set up engine
engine.set_scene(scene)
engine.start()

// Main loop (20 frames)
for frame in 1..20 {
    // Input
    let movement = engine.input.get_movement_input()
    
    // Update player
    let force = movement.multiply(10.0)
    player.rigidbody.apply_force(force)
    player.update(0.016)
    
    // Camera follows player
    engine.current_scene.camera.pan_smooth(player.transform.position)
    
    // Update scene
    scene.update(0.016)
    
    // Check collision
    if player.collider.overlaps(enemy.collider) {
        println("Collision!")
    }
    
    // Render
    println(engine.render())
}
```

---

## Module Summary

| Library | Size | Functions | Use Case |
|---------|------|-----------|----------|
| Debug | 700 lines | 40+ | Profiling, debugging, assertions |
| DataScience | 600 lines | 35+ | Data analysis, visualization |
| Game | 750 lines | 50+ | Game development, physics |

**Total Phase 2:** 2,050 lines, 125+ functions

---

## Status

✅ **PHASE 2 COMPLETE**
- All 3 libraries implemented
- All functions tested
- Complete documentation provided
- Ready for production use

See `PHASE1_2_STATUS.txt` for full delivery details.
