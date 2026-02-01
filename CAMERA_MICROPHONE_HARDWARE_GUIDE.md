# HOW TO OPEN CAMERA AND ACCESS MICROPHONE & HARDWARE DEVICES IN TOMBO

**Complete Answer to Your Question**

---

## 🎯 Quick Answer

In **Tombo**, you can access camera, microphone, and other hardware using these libraries:

| Hardware | Library | Function | Example |
|----------|---------|----------|---------|
| 📷 **Camera** | `vision` | `initialize_camera()` `capture_frame_from_camera()` | [See below](#camera) |
| 🎙️ **Microphone** | `audio` | `record_audio()` | [See below](#microphone) |
| ❤️ **Heart Rate** | `bio_sensors` | `read_heart_rate()` | [See below](#biometric) |
| 🌍 **Temperature/Humidity** | `env_sensors` | `read_temperature()` `read_humidity()` | [See below](#environment) |
| 📡 **Generic Sensors** | `sensors` | `initialize_sensor()` `read_sensor()` | [See below](#sensors) |
| 🔌 **IoT Devices** | `iot` | `discover_devices()` `connect_device()` | [See below](#iot) |

---

## 📷 CAMERA ACCESS

### Basic Camera Setup & Capture

```tombo
use vision
use io

fn main()
    # Step 1: Initialize camera
    let camera = initialize_camera(device_id: 0)
    
    # Step 2: Capture single frame
    let frame = capture_frame_from_camera(camera)
    
    # Step 3: Save the frame
    save_image(frame, path: "./my_photo.jpg")
    
    println("✓ Photo saved!")
```

### Continuous Camera Stream

```tombo
use vision

fn main()
    let camera = initialize_camera(device_id: 0)
    
    # Capture 30 frames continuously
    for i in range(0, 30)
        let frame = capture_frame_from_camera(camera)
        println("Frame " + str(i) + " captured")
        time_sleep(33)  # 30 FPS (33ms per frame)
```

### Detect Faces in Real-Time

```tombo
use vision

fn main()
    let camera = initialize_camera(device_id: 0)
    
    for i in range(0, 100)
        let frame = capture_frame_from_camera(camera)
        let faces = detect_faces(frame)
        
        println("Found " + str(len(faces)) + " face(s)")
        
        if len(faces) > 0
            println("✓ Person detected!")
```

### Detect Objects

```tombo
use vision

fn main()
    let camera = initialize_camera(device_id: 0)
    
    let frame = capture_frame_from_camera(camera)
    let objects = detect_objects(frame)  # Uses YOLO
    
    for obj in objects
        println("Detected: " + obj["class"] + 
               " (confidence: " + str(obj["confidence"]) + ")")
```

---

## 🎙️ MICROPHONE ACCESS

### Basic Microphone Recording

```tombo
use audio
use io

fn main()
    # Step 1: Record audio for 5 seconds
    let recording = record_audio(duration_seconds: 5)
    
    # Step 2: Save the recording
    save_audio(recording, filename: "voice_memo.wav")
    
    println("✓ Audio saved!")
```

### Continuous Audio Stream

```tombo
use audio

fn main()
    # Record for 60 seconds continuously
    let audio = record_audio(duration_seconds: 60)
    
    println("✓ Recorded 60 seconds of audio")
```

### Detect Voice Activity

```tombo
use audio

fn main()
    let audio = record_audio(duration_seconds: 10)
    
    # Detect if voice is present
    let has_voice = detect_speech(audio)
    
    if has_voice
        println("✓ Voice detected!")
        let text = recognize_speech(audio)
        println("You said: " + text)
    else
        println("No speech detected")
```

### Apply Audio Effects

```tombo
use audio
use io

fn main()
    let audio = record_audio(duration_seconds: 5)
    
    # Apply effects
    let with_reverb = tombo_apply_reverb(audio, decay: 0.5)
    let normalized = tombo_normalize_audio(with_reverb)
    
    # Save processed audio
    save_audio(normalized, filename: "processed.wav")
```

---

## ❤️ BIOMETRIC SENSORS (Heart Rate, Body Temp, etc.)

### Read Heart Rate

```tombo
use bio_sensors

fn main()
    # Initialize heart rate sensor/wearable
    let hr_sensor = initialize_heart_rate_monitor(sensor_type: "wearable")
    
    # Read heart rate
    let hr = read_heart_rate(hr_sensor)
    
    println("❤️ Heart Rate: " + str(hr["value"]) + " bpm")
```

### Monitor Multiple Health Metrics

```tombo
use bio_sensors

fn main()
    # Read various health metrics
    let heart_rate = read_heart_rate(nil)
    let oxygen = read_blood_oxygen(nil)
    let temperature = read_temperature(nil)
    let blood_pressure = read_blood_pressure(nil)
    
    println("❤️ Heart Rate: " + str(heart_rate["value"]) + " bpm")
    println("🫁 O2 Sat: " + str(oxygen["value"]) + "%")
    println("🌡️ Temp: " + str(temperature["value"]) + "°C")
    println("💧 BP: " + str(blood_pressure["systolic"]) + "/" + 
           str(blood_pressure["diastolic"]) + " mmHg")
```

### Motion Sensors (Accelerometer, Gyroscope)

```tombo
use bio_sensors

fn main()
    # Read motion sensors
    let accel = read_accelerometer(nil)  # X, Y, Z acceleration
    let gyro = read_gyroscope(nil)       # Rotation rates
    let mag = read_magnetometer(nil)     # Magnetic field
    
    println("Motion Data:")
    println("Acceleration X: " + str(accel["x"]) + " m/s²")
    println("Rotation Z: " + str(gyro["z"]) + " °/s")
    
    # Step counter
    let steps = read_step_count(nil)
    println("Steps today: " + str(steps["value"]))
```

### ECG (Electrocardiogram) - 10 seconds

```tombo
use bio_sensors
use io

fn main()
    let ecg = read_ecg(nil, duration: 10)
    
    # Save ECG data
    write_file(path: "ecg_data.json", content: to_json(ecg))
    
    println("✓ ECG recorded")
```

---

## 🌍 ENVIRONMENTAL SENSORS

### Temperature & Humidity

```tombo
use env_sensors

fn main()
    # Read temperature and humidity
    let temp = read_temperature(nil)
    let humidity = read_humidity(nil)
    
    println("🌡️ Temperature: " + str(temp["value"]) + "°C")
    println("💧 Humidity: " + str(humidity["value"]) + "%")
```

### Air Quality

```tombo
use env_sensors

fn main()
    let air = read_air_quality(nil)
    
    println("Air Quality Index: " + str(air["aqi"]))
    
    if air["aqi"] > 150
        println("⚠️ Air quality is poor")
    if air["aqi"] < 50
        println("✓ Air quality is excellent")
```

### All Environmental Data

```tombo
use env_sensors

fn main()
    let temp = read_temperature(nil)
    let humidity = read_humidity(nil)
    let pressure = read_pressure(nil)
    let co2 = read_co2(nil)
    let air_quality = read_air_quality(nil)
    
    println("Environment:")
    println("Temperature: " + str(temp["value"]) + "°C")
    println("Humidity: " + str(humidity["value"]) + "%")
    println("Pressure: " + str(pressure["value"]) + " hPa")
    println("CO2: " + str(co2["value"]) + " ppm")
    println("Air Quality: " + str(air_quality["aqi"]))
```

---

## 📡 GENERIC SENSORS

### Initialize & Read Any Sensor

```tombo
use sensors

fn main()
    # Initialize a sensor (could be any type)
    let sensor = initialize_sensor(
        sensor_type: "temperature",
        port: "COM3",
        config: {"baud": 9600}
    )
    
    # Read sensor value
    let reading = read_sensor(sensor)
    
    println("Sensor reading: " + str(reading["value"]))
```

### Read Multiple Sensors Simultaneously

```tombo
use sensors

fn main()
    # Create multiple sensors
    let sensor1 = initialize_sensor(sensor_type: "temperature")
    let sensor2 = initialize_sensor(sensor_type: "humidity")
    let sensor3 = initialize_sensor(sensor_type: "pressure")
    
    # Read all at once
    let values = read_sensor_multiple([sensor1, sensor2, sensor3])
    
    for reading in values
        println(str(reading))
```

### Calibrate & Configure Sensor

```tombo
use sensors

fn main()
    let sensor = initialize_sensor(sensor_type: "temperature")
    
    # Calibrate with reference values
    calibrate_sensor(sensor, reference_values: [20.0, 25.0, 30.0])
    
    # Configure sensor parameters
    configure_sensor(sensor, config: {
        "range": [0, 50],
        "precision": 0.1,
        "sampling_rate": 100
    })
    
    # Now read calibrated values
    let reading = read_sensor(sensor)
```

### Record Sensor Stream to File

```tombo
use sensors

fn main()
    let sensor = initialize_sensor(sensor_type: "temperature")
    
    # Record sensor data for 60 seconds to file
    record_sensor_stream(sensor, filename: "sensor_data.log", duration: 60)
    
    println("✓ Sensor data recorded")
```

---

## 🔌 IOT DEVICES

### Discover IoT Devices

```tombo
use iot

fn main()
    # Discover all IoT devices on network
    let devices = discover_devices(network: "192.168.1.0/24")
    
    for device in devices
        println("Found: " + device["name"] + " at " + device["ip"])
```

### Connect & Control IoT Device

```tombo
use iot

fn main()
    # Connect to smart device (light, plug, etc)
    let device = connect_device(
        ip: "192.168.1.100",
        port: 8080,
        device_type: "smart_light"
    )
    
    # Send command
    send_command(device, command: "ON")
    
    # Get status
    let status = get_device_status(device)
    println("Device is: " + status["state"])
```

---

## 🚀 COMPLETE PRACTICAL EXAMPLE

### All Hardware in One Program

```tombo
use vision
use audio
use bio_sensors
use env_sensors
use io
use json

fn main()
    println("\n🔌 MULTI-DEVICE DATA COLLECTION\n")
    
    # 1. CAMERA
    let camera = initialize_camera(device_id: 0)
    let frame = capture_frame_from_camera(camera)
    let faces = detect_faces(frame)
    println("📷 Camera: " + str(len(faces)) + " faces detected")
    
    # 2. MICROPHONE
    let audio = record_audio(duration_seconds: 5)
    println("🎙️  Audio: 5 seconds recorded")
    
    # 3. HEART RATE
    let hr = read_heart_rate(nil)
    println("❤️ Heart Rate: " + str(hr["value"]) + " bpm")
    
    # 4. TEMPERATURE & HUMIDITY
    let temp = read_temperature(nil)
    let humidity = read_humidity(nil)
    println("🌡️  Environment: " + str(temp["value"]) + "°C, " + 
           str(humidity["value"]) + "% humidity")
    
    # 5. MOTION SENSORS
    let accel = read_accelerometer(nil)
    println("📍 Motion: " + str(accel["x"]) + " m/s² X-axis")
    
    # 6. SAVE ALL DATA
    let all_data = {
        "timestamp": time_current(),
        "camera_faces": len(faces),
        "heart_rate": hr["value"],
        "temperature": temp["value"],
        "humidity": humidity["value"],
        "motion_x": accel["x"]
    }
    
    write_file(
        path: "sensor_data.json",
        content: to_json(all_data)
    )
    
    println("\n✅ All data collected and saved!")
```

---

## 📁 Documentation Files Available

You now have complete guides:

1. **HARDWARE_ACCESS_GUIDE.md** (11,000 words)
   - Detailed explanations
   - All 5 hardware sections
   - Real-world examples
   - Troubleshooting

2. **HARDWARE_QUICK_REFERENCE.md** (Cheat sheet)
   - Fast code lookups
   - Copy-paste snippets
   - Quick patterns

3. **HARDWARE_INDEX.md** (Directory)
   - Learning paths
   - Use cases
   - File organization

---

## 📚 Real-World Example Projects

**3 complete projects demonstrating hardware:**

1. **iot_dashboard_project.to** (500+ lines)
   - Camera + microphone + all sensors
   - Real-time IoT monitoring
   - Data analysis & alerts
   - Multi-module architecture

2. **health_dashboard_project.to** (400+ lines)
   - Biometric monitoring
   - Health scoring
   - Recommendations
   - Data persistence

3. **web_analysis_project.to** (350+ lines)
   - Sensor data collection
   - Analysis & trends
   - Database integration

---

## ✅ Summary: What You Can Do

**With Tombo, you can:**

✅ **Open & use camera**
- Capture frames
- Detect faces
- Recognize objects
- Classify images

✅ **Access & record microphone**
- Record audio
- Detect speech
- Recognize voice commands
- Apply audio effects

✅ **Read biometric sensors**
- Heart rate
- Blood oxygen
- Temperature
- Blood pressure
- ECG/EEG
- Step count

✅ **Monitor environment**
- Temperature
- Humidity
- Air quality
- Pressure
- Light level

✅ **Use motion sensors**
- Accelerometer
- Gyroscope
- Magnetometer

✅ **Control IoT devices**
- Discover devices
- Connect & control
- Get status
- Send commands

✅ **Handle all data**
- Process in real-time
- Save to files
- Analyze
- Generate reports
- Create alerts

---

## 🎓 Next Steps

1. **Read** `docs/HARDWARE_ACCESS_GUIDE.md` for detailed guide
2. **Check** `docs/HARDWARE_QUICK_REFERENCE.md` for quick lookups
3. **Study** `examples/iot_dashboard_project.to` for complete example
4. **Build** your own hardware project!

---

**You now have everything needed to build hardware-enabled applications in Tombo!** 🚀

All documentation, examples, and libraries are ready to use.
