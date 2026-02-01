# TOMBO NEW LIBRARIES - QUICK START GUIDE

## 5 Powerful Libraries Just Added

### 1. Scientific Library - Advanced Computing

```tombo
use scientific

# LINEAR ALGEBRA
let A = matrix([[1, 2], [3, 4]])
let det = A.determinant()           # Calculate determinant: -2
let inv = A.inverse()                # Calculate inverse
let transposed = A.transpose()        # Transpose matrix
let trace = A.trace()                 # Sum of diagonal

# VECTORS
let v1 = vector([1, 2, 3])
let v2 = vector([4, 5, 6])
let sum = v1.add(v2)                  # Add vectors
let dot_prod = v1.dot(v2)             # Dot product: 32
let cross_prod = v1.cross(v2)         # Cross product
let mag = v1.magnitude()               # Length of vector
let normalized = v1.normalize()        # Unit vector

# STATISTICS
let data = [1, 2, 3, 4, 5, 10, 20]
println(mean(data))                    # 6.43 (average)
println(median(data))                  # 4.0 (middle value)
println(std(data))                     # 7.2 (spread)
println(variance(data))                # 51.9 (variance)

# CORRELATION
let x_values = [1, 2, 3, 4, 5]
let y_values = [2, 4, 6, 8, 10]
let r = correlation(x_values, y_values) # Perfect correlation: 1.0

# SIGNAL PROCESSING
let signal = [sin(0), sin(0.1), sin(0.2), ...]
let spectrum = fft(signal)              # Fast Fourier Transform
let power = power_spectrum(signal)      # Power spectrum

# OPTIMIZATION
def f(x)
    return x^2 + 4*x + 4              # (x+2)^2
end

def grad_f(x)
    return 2*x + 4                    # Derivative
end

let minimum = minimize(f, grad_f, x0=0)  # Find minimum point
```

### 2. Audio Library - Sound Processing

```tombo
use audio

# SYNTHESIS - Generate Waveforms
let sine = generate_sine(440, 2.0)        # A4 note for 2 seconds
let square = generate_square(440, 2.0)    # Square wave
let sawtooth = generate_sawtooth(440, 2.0) # Sawtooth wave
let triangle = generate_triangle(440, 2.0) # Triangle wave

# RECORDING & PLAYBACK
stream = record_audio(duration=5.0)        # Record 5 seconds
play_audio(stream)                         # Play recording

# FILTERING
let voice_data = load_audio("voice.wav")
let cleaned = filter_lowpass(voice_data, 5000)      # Remove high noise
let enhanced = filter_highpass(voice_data, 200)     # Remove rumble
let bandpass = filter_bandpass(voice_data, 200, 5000) # Keep speech range

# ANALYSIS
let rms = analyze_rms(voice_data)          # Volume level (0-1)
let peak = analyze_peak(voice_data)        # Loudest point
let zeros = analyze_zero_crossings(voice_data) # Zero crossings (for pitch)

# ENVELOPE (ADSR)
envelope = create_envelope(
    attack=0.1,    # Fade in: 100ms
    decay=0.2,     # Decay: 200ms
    sustain=0.7,   # Hold at 70%: 
    release=0.5    # Fade out: 500ms
)
let shaped = envelope.apply(sine_wave, note_duration=2.0)

# CREATE MUSIC
def play_note(frequency, duration)
    let wave = generate_sine(frequency, duration)
    let env_shaped = envelope.apply(wave, duration)
    play_audio(env_shaped)
end

play_note(440, 1.0)    # A4
play_note(494, 1.0)    # B4
play_note(523, 1.0)    # C5
```

### 3. Image Library - Image Processing

```tombo
use image

# CREATE & LOAD IMAGES
image = create_image(800, 600, (255, 255, 255))  # White 800x600
image = load_image("photo.jpg")                   # Load from file
save_image(image, "output.jpg")                   # Save to file

# TRANSFORMATIONS
resized = resize_image(image, 400, 300)           # Scale to 400x300
cropped = crop_image(image, 100, 100, 500, 500)  # Crop to region
rotated = rotate_image(image, 90)                 # Rotate 90° clockwise
h_flip = flip_horizontal(image)                   # Mirror horizontally
v_flip = flip_vertical(image)                     # Mirror vertically

# COLOR & TONE
gray = grayscale(image)                           # Convert to black & white
sepia = sepia(image)                              # Vintage sepia tone
inverted = invert(image)                          # Negative image

# FILTERS & EFFECTS
blurred = blur(image, kernel_size=5)              # Blur image
sharpened = sharpen(image)                        # Enhance edges
edges = detect_edges(image)                       # Find edges (Sobel)
binary = threshold(image, threshold_val=128)      # B&W threshold

# ADJUSTMENTS
brighter = adjust_brightness(image, 1.5)          # 50% brighter
darker = adjust_brightness(image, 0.5)            # 50% darker
high_contrast = adjust_contrast(image, 1.5)       # Increase contrast
low_contrast = adjust_contrast(image, 0.8)        # Decrease contrast

# ANALYSIS
histogram = get_histogram(image)
red_channel = histogram["red"]       # Red color distribution
green_channel = histogram["green"]   # Green color distribution
blue_channel = histogram["blue"]     # Blue color distribution

# EXAMPLE: Convert to B&W and detect edges
def find_image_features(image_path)
    let img = load_image(image_path)
    let gray = grayscale(img)
    let edges = detect_edges(gray)
    save_image(edges, "edges_" + image_path)
end
```

### 4. Network Library - Networking

```tombo
use network

# DNS RESOLUTION
let ip = gethostbyname("example.com")      # "93.184.216.34"
let hostname = gethostbyaddr("8.8.8.8")[0] # "dns.google"

# NETWORK DIAGNOSTICS
latency = ping("example.com")               # Get ping time (ms)
route = traceroute("example.com")           # Trace route to host

# PORT SCANNING
open_ports = scan_ports("192.168.1.1", 1, 1024)  # Scan common ports
is_open = scan_port("192.168.1.1", 22)     # Check SSH port

# SPEED TESTING
download_speed = test_bandwidth("https://speed.example.com")  # Mbps
latency = test_latency("8.8.8.8")          # Ping time (ms)

# PACKET CAPTURE
packets = sniff_packets(interface="eth0")   # Capture network packets
for packet in packets
    println("From: " + packet.src_ip + " To: " + packet.dst_ip)
end

# HTTP REQUESTS
response = http_get("https://api.example.com/data")
println(response.status)        # 200
println(response.body)          # Response content

data = {"name": "Alice", "age": 30}
response = http_post("https://api.example.com/users", data)

# CREATE SERVER
socket = create_tcp_socket()
socket.bind("localhost", 8080)
socket.listen()

# EXAMPLE: Simple Network Monitor
def monitor_connection()
    for i in 0..10
        latency = ping("1.1.1.1")
        if latency > 100
            println("High latency: " + latency + "ms")
        end
        sleep(5)
    end
end
```

### 5. Concurrency Library - Multi-threading & Async

```tombo
use concurrency

# CREATE THREADS
def worker(task_id)
    for i in 0..10
        println("Task " + task_id + " step " + i)
        sleep(0.5)
    end
end

t1 = create_thread(target=worker, args=(1,))
t2 = create_thread(target=worker, args=(2,))

t1.start()
t2.start()

result1 = t1.get_result()      # Wait for thread
result2 = t2.get_result()

# THREAD POOLS
def expensive_computation(x)
    return x * x + sqrt(x)
end

# Run 100 computations in parallel
items = range(1, 101)
results = run_in_parallel(expensive_computation, items, num_workers=4)
println("Results: " + results)

# LOCKS & SYNCHRONIZATION
lock = create_lock()

shared_counter = 0

def increment()
    with lock
        shared_counter = shared_counter + 1
    end
end

# SEMAPHORE (Limit concurrent access)
db_connections = create_semaphore(count=5)  # Max 5 connections

def query_database()
    with db_connections
        # Execute database query (only 5 at a time)
    end
end

# EVENT SIGNALING
event = create_event()

def waiter()
    println("Waiting for event...")
    event.wait()
    println("Event triggered!")
end

def signaler()
    sleep(5)
    event.set()
end

t1 = create_thread(waiter)
t2 = create_thread(signaler)
t1.start()
t2.start()

# PARALLEL LOOP
def process_item(index)
    println("Processing item " + index)
    # Do work
end

parallel_for(process_item, start=0, end=100, num_workers=4)

# EXAMPLE: Parallel Web Scraping
def fetch_url(url)
    let response = http_get(url)
    return response.body
end

urls = [
    "https://api.github.com/users/torvalds",
    "https://api.github.com/users/guido",
    "https://api.github.com/users/dhh"
]

results = run_in_parallel(fetch_url, urls, num_workers=3)
```

---

## 🔥 Combined Example: Image + Scientific Analysis

```tombo
use image
use scientific

# Load image and analyze
photo = load_image("photo.jpg")

# Convert to grayscale and extract edge features
gray = grayscale(photo)
edges = detect_edges(gray)

# Analyze the histogram
histogram = get_histogram(photo)

# Calculate statistics on color distribution
red_dist = histogram["red"]
mean_red = mean(red_dist)
std_red = std(red_dist)

println("Red channel: mean=" + mean_red + ", std=" + std_red)

# Save processed image
save_image(edges, "edges.jpg")
```

---

## 🚀 Combined Example: Audio + Concurrency

```tombo
use audio
use concurrency

# Generate multiple notes in parallel
def generate_note(frequency, duration)
    return generate_sine(frequency, duration)
end

frequencies = [440, 494, 523, 587]  # A, B, C, D

notes = run_in_parallel(generate_note, frequencies, num_workers=4)

# Mix and play
for note in notes
    play_audio(note)
end
```

---

## 📊 Combined Example: Network + Concurrency

```tombo
use network
use concurrency

# Check multiple servers in parallel
def check_server(host)
    return {
        "host": host,
        "latency": ping(host),
        "online": ping(host) != null
    }
end

servers = [
    "8.8.8.8",
    "1.1.1.1",
    "208.67.222.222"
]

results = run_in_parallel(check_server, servers, num_workers=3)

for result in results
    if result.online
        println(result.host + " is online (latency: " + result.latency + "ms)")
    else
        println(result.host + " is offline")
    end
end
```

---

## 📚 Library Statistics

| Library | Classes | Functions | Use Case |
|---------|---------|-----------|----------|
| **Scientific** | 5 | 40+ | Math, linear algebra, stats, signals |
| **Audio** | 8 | 35+ | Sound synthesis, recording, analysis |
| **Image** | 2 | 35+ | Image processing, filters, analysis |
| **Network** | 8 | 40+ | Networking, DNS, HTTP, diagnostics |
| **Concurrency** | 10 | 45+ | Threading, async, parallelism |
| **TOTAL** | **33** | **195+** | Complete computing toolkit |

---

## 🎯 What's Next?

After these 5 libraries, the next batch will include:
- **Testing Framework** - Unit tests, assertions, test runners
- **Debug Library** - Debugger, profiler, memory analysis
- **DataScience** - DataFrames, data manipulation
- **Game Engine** - Graphics, physics, input handling
- **Mobile** - UI, sensors, notifications

**All 63 libraries coming soon!**

---

*Generated: February 1, 2026*
*TOMBO Language v1.0.0*
