# Hardware Access Guide - Tombo Language

**A comprehensive guide to accessing camera, microphone, and other hardware devices in Tombo**

---

## Table of Contents

1. [Overview](#overview)
2. [Camera Access](#camera-access)
3. [Microphone Access](#microphone-access)
4. [Hardware Sensors](#hardware-sensors)
5. [Device Integration](#device-integration)
6. [Real-World Examples](#real-world-examples)
7. [Troubleshooting](#troubleshooting)

---

## Overview

Tombo provides **39 libraries** with **1,327+ functions** for hardware access. The main libraries for hardware interaction are:

| Library | Purpose | Hardware Access |
|---------|---------|-----------------|
| **vision** | Camera & image processing | 📷 Camera capture, image analysis |
| **audio** | Microphone & sound processing | 🎙️ Microphone input, audio recording |
| **sensors** | General sensor access | 📡 Any sensor integration |
| **bio_sensors** | Health & motion sensors | ❤️ Heart rate, accelerometer, etc. |
| **iot** | IoT device management | 🔌 Connected devices |
| **concurrency** | Multi-threaded hardware access | ⚡ Parallel device polling |

---

## Camera Access

### Basic Camera Operations

**1. Initialize Camera**
```tombo
use vision

fn initialize_camera() -> Dict
    # Open default camera (0)
    let camera = initialize_camera(device_id: 0)
    return camera

fn main()
    let camera = initialize_camera()
    println("✓ Camera initialized: " + str(camera))
```

**2. Capture Single Frame**
```tombo
use vision

fn capture_frame(camera: Dict) -> Dict
    # Capture one frame from camera
    let frame = capture_frame_from_camera(camera)
    
    # Get frame dimensions
    let width = get_image_dimensions(frame)[0]
    let height = get_image_dimensions(frame)[1]
    
    println("📸 Captured frame: " + str(width) + "x" + str(height))
    return frame

fn main()
    let camera = initialize_camera(device_id: 0)
    let frame = capture_frame(camera)
    save_image(frame, path: "./captured_frame.jpg")
    println("✓ Frame saved!")
```

**3. Continuous Video Stream**
```tombo
use vision
use io

fn stream_video(camera: Dict, duration_seconds: Int) -> List
    """Capture continuous video stream"""
    let frames = []
    let start_time = time_current()
    
    while time_elapsed() < duration_seconds
        let frame = capture_frame_from_camera(camera)
        frames = append(frames, frame)
        
        # Show status
        let fps = len(frames) / time_elapsed()
        println("Recording... FPS: " + str(fps))
    
    return frames

fn main()
    let camera = initialize_camera(device_id: 0)
    
    # Record 10 seconds of video
    let video_frames = stream_video(camera, duration_seconds: 10)
    
    println("✓ Recorded " + str(len(video_frames)) + " frames")
```

### Image Processing with Camera

**4. Real-Time Face Detection**
```tombo
use vision

fn detect_faces_realtime(camera: Dict, max_duration: Int = 30) -> List
    """Detect faces in camera stream"""
    let faces_detected = []
    let start_time = time_current()
    
    while time_elapsed() < max_duration
        let frame = capture_frame_from_camera(camera)
        let faces = detect_faces(frame)
        
        if len(faces) > 0
            faces_detected = append(faces_detected, {
                "timestamp": time_current(),
                "count": len(faces),
                "faces": faces
            })
            
            println("✓ Detected " + str(len(faces)) + " face(s)")
    
    return faces_detected

fn main()
    let camera = initialize_camera(device_id: 0)
    let detections = detect_faces_realtime(camera)
    println("Total detections: " + str(len(detections)))
```

**5. Object Detection from Camera**
```tombo
use vision

fn detect_objects_stream(camera: Dict) -> Dict
    """Detect objects in real-time"""
    let results = {
        "total_frames": 0,
        "detections": []
    }
    
    for i in range(0, 100)  # Process 100 frames
        let frame = capture_frame_from_camera(camera)
        
        # Detect objects using YOLOv3 or similar
        let objects = detect_objects(frame)
        
        results["total_frames"] = results["total_frames"] + 1
        results["detections"] = append(results["detections"], objects)
        
        # Print detected objects
        for obj in objects
            println("🔍 Found: " + obj["class"] + " (confidence: " + str(obj["confidence"]) + ")")
    
    return results

fn main()
    let camera = initialize_camera(device_id: 0)
    detect_objects_stream(camera)
```

**6. Image Classification**
```tombo
use vision

fn classify_camera_feed(camera: Dict) -> List
    """Classify images from camera"""
    let classifications = []
    
    for frame_num in range(0, 50)
        let frame = capture_frame_from_camera(camera)
        let prediction = classify_image(frame)
        
        classifications = append(classifications, {
            "frame": frame_num,
            "class": prediction["class"],
            "confidence": prediction["confidence"],
            "top_5": prediction["top_5_predictions"]
        })
        
        println("Frame " + str(frame_num) + ": " + prediction["class"])
    
    return classifications

fn main()
    let camera = initialize_camera(device_id: 0)
    let results = classify_camera_feed(camera)
```

---

## Microphone Access

### Basic Microphone Operations

**1. Initialize Microphone**
```tombo
use audio

fn initialize_microphone() -> Dict
    """Initialize microphone for audio recording"""
    # Default microphone (device 0)
    let microphone = {
        "type": "microphone",
        "device_id": 0,
        "sample_rate": 44100,
        "channels": 1,
        "format": "PCM_16"
    }
    
    println("✓ Microphone initialized at 44.1 kHz")
    return microphone

fn main()
    let mic = initialize_microphone()
```

**2. Record Audio**
```tombo
use audio
use io

fn record_audio(duration_seconds: Int) -> Dict
    """Record audio for specified duration"""
    let recording = {
        "sample_rate": 44100,
        "duration": duration_seconds,
        "samples": []
    }
    
    println("🎙️ Recording for " + str(duration_seconds) + " seconds...")
    
    let start = time_current()
    while time_elapsed() < duration_seconds
        # Simulate capturing audio samples
        let chunk = capture_audio_chunk()
        recording["samples"] = append(recording["samples"], chunk)
        
        let elapsed = time_elapsed()
        println("Recorded: " + str(elapsed) + " seconds")
    
    return recording

fn capture_audio_chunk() -> Dict
    return {"samples": [0, 1, -1, 2, -2]}

fn main()
    let audio = record_audio(duration_seconds: 5)
    save_audio(audio, filename: "./recording.wav")
    println("✓ Audio saved!")
```

**3. Real-Time Audio Level Monitoring**
```tombo
use audio

fn monitor_audio_levels(duration_seconds: Int) -> Dict
    """Monitor microphone levels in real-time"""
    let levels = {
        "min": 0,
        "max": 0,
        "average": 0,
        "readings": []
    }
    
    let sum = 0
    let count = 0
    
    for i in range(0, duration_seconds * 100)  # 100ms intervals
        let chunk = capture_audio_chunk()
        let level = get_audio_level(chunk)
        
        levels["readings"] = append(levels["readings"], level)
        sum = sum + level
        count = count + 1
        
        if level < levels["min"]
            levels["min"] = level
        if level > levels["max"]
            levels["max"] = level
        
        # Visual indicator
        let bar = ""
        for j in range(0, level)
            bar = bar + "█"
        println("Level: " + bar)
    
    levels["average"] = sum / count
    return levels

fn get_audio_level(chunk: Dict) -> Int
    return 50  # Simulated level

fn main()
    let levels = monitor_audio_levels(duration_seconds: 10)
    println("\n📊 Audio Statistics:")
    println("Min: " + str(levels["min"]))
    println("Max: " + str(levels["max"]))
    println("Avg: " + str(levels["average"]))
```

**4. Voice Detection**
```tombo
use audio

fn detect_voice_activity(duration_seconds: Int) -> List
    """Detect when voice is present in audio stream"""
    let voice_segments = []
    let is_voice = false
    let segment_start = 0
    
    for i in range(0, duration_seconds)
        let chunk = capture_audio_chunk()
        let has_voice = detect_speech(chunk)
        
        if has_voice and not is_voice
            # Voice started
            segment_start = i
            is_voice = true
            println("🎤 Voice detected at " + str(i) + "s")
        
        if not has_voice and is_voice
            # Voice ended
            voice_segments = append(voice_segments, {
                "start": segment_start,
                "end": i,
                "duration": i - segment_start
            })
            is_voice = false
            println("✓ Voice segment: " + str(segment_start) + "s to " + str(i) + "s")
    
    return voice_segments

fn detect_speech(chunk: Dict) -> Bool
    return true  # Simulated

fn main()
    let segments = detect_voice_activity(duration_seconds: 30)
    println("\nFound " + str(len(segments)) + " voice segments")
```

**5. Audio Effects & Processing**
```tombo
use audio

fn apply_effects_to_audio(audio: Dict) -> Dict
    """Apply audio effects to recorded audio"""
    
    # Normalize
    let normalized = tombo_normalize_audio(audio)
    println("✓ Applied normalization")
    
    # Add fade in
    normalized = tombo_apply_fade_in(normalized, duration: 0.5)
    println("✓ Applied fade in")
    
    # Add reverb
    normalized = tombo_apply_reverb(normalized, decay: 0.6)
    println("✓ Applied reverb")
    
    # Compress
    normalized = tombo_apply_compression(normalized, threshold: -20, ratio: 4)
    println("✓ Applied compression")
    
    return normalized

fn main()
    let raw_audio = record_audio(duration_seconds: 5)
    let processed = apply_effects_to_audio(raw_audio)
    save_audio(processed, filename: "./processed_audio.wav")
```

---

## Hardware Sensors

### Sensor Types & Access

**1. Motion Sensors (Accelerometer, Gyroscope)**
```tombo
use bio_sensors

fn read_motion_sensors() -> Dict
    """Read motion from device sensors"""
    let motion = {
        "acceleration": read_accelerometer(nil),
        "rotation": read_gyroscope(nil),
        "magnetic_field": read_magnetometer(nil)
    }
    
    println("📍 Motion Data:")
    println("Acceleration X: " + str(motion["acceleration"]["x"]) + " m/s²")
    println("Rotation Z: " + str(motion["rotation"]["z"]) + " °/s")
    
    return motion

fn main()
    for i in range(0, 10)
        let data = read_motion_sensors()
        time_sleep(100)  # 100ms delay
```

**2. Environmental Sensors**
```tombo
use env_sensors

fn read_environment() -> Dict
    """Read environmental sensors"""
    let environment = {
        "temperature": read_temperature(nil),
        "humidity": read_humidity(nil),
        "pressure": read_pressure(nil),
        "air_quality": read_air_quality(nil),
        "uv_index": read_uv_index(nil)
    }
    
    println("🌍 Environment:")
    println("Temperature: " + str(environment["temperature"]) + "°C")
    println("Humidity: " + str(environment["humidity"]) + "%")
    println("Air Quality Index: " + str(environment["air_quality"]["aqi"]))
    
    return environment

fn main()
    read_environment()
```

**3. Biometric Sensors**
```tombo
use bio_sensors

fn read_health_metrics() -> Dict
    """Read biometric health data"""
    let health = {
        "heart_rate": read_heart_rate(nil),
        "blood_oxygen": read_blood_oxygen(nil),
        "temperature": read_temperature(nil),
        "steps": read_step_count(nil),
        "calories": read_calories_burned(nil)
    }
    
    println("❤️  Health Metrics:")
    println("Heart Rate: " + str(health["heart_rate"]["value"]) + " bpm")
    println("O2 Saturation: " + str(health["blood_oxygen"]["value"]) + "%")
    println("Body Temp: " + str(health["temperature"]["value"]) + "°C")
    println("Steps: " + str(health["steps"]["value"]))
    println("Calories: " + str(health["calories"]["value"]) + " kcal")
    
    return health

fn main()
    read_health_metrics()
```

**4. GPS/Location Sensor**
```tombo
use iot

fn read_gps_location() -> Dict
    """Read GPS coordinates"""
    let location = {
        "latitude": 0.0,
        "longitude": 0.0,
        "altitude": 0.0,
        "accuracy": 0.0,
        "timestamp": 0
    }
    
    println("📡 GPS Location:")
    println("Lat: " + str(location["latitude"]))
    println("Lon: " + str(location["longitude"]))
    println("Alt: " + str(location["altitude"]) + "m")
    
    return location

fn main()
    read_gps_location()
```

---

## Device Integration

### Multi-Device Synchronization

**1. Synchronized Multi-Sensor Reading**
```tombo
use sensors
use concurrency

fn read_multiple_sensors_sync() -> Dict
    """Read from camera, microphone, and sensors simultaneously"""
    
    let results = {
        "camera_frame": nil,
        "audio_chunk": nil,
        "motion_data": nil,
        "env_data": nil,
        "timestamp": time_current()
    }
    
    # All in parallel (simulated)
    results["camera_frame"] = capture_frame_from_camera(nil)
    results["audio_chunk"] = capture_audio_chunk()
    results["motion_data"] = read_accelerometer(nil)
    results["env_data"] = read_temperature(nil)
    
    println("✓ All devices read at: " + str(results["timestamp"]))
    return results

fn main()
    for i in range(0, 100)
        read_multiple_sensors_sync()
        time_sleep(33)  # ~30fps
```

**2. Sensor Fusion (Combining Multiple Sources)**
```tombo
use bio_sensors
use vision

fn fuse_sensor_data(camera: Dict, sensors: List) -> Dict
    """Combine data from multiple sensors"""
    
    let frame = capture_frame_from_camera(camera)
    let detected_faces = detect_faces(frame)
    let heart_rate = read_heart_rate(nil)
    let stress_level = read_galvanic_skin_response(nil)
    
    let fused = {
        "faces_detected": len(detected_faces),
        "heart_rate": heart_rate["value"],
        "stress_indicator": stress_level["value"],
        "activity_level": "normal",
        "confidence": 0.92
    }
    
    # Compute overall state
    if heart_rate["value"] > 100
        fused["activity_level"] = "elevated"
    
    println("🔗 Fused Data: " + str(fused))
    return fused

fn main()
    let camera = initialize_camera(device_id: 0)
    fuse_sensor_data(camera, [])
```

---

## Real-World Examples

### Example 1: Security Camera System

```tombo
use vision
use io
use json
use time

fn security_camera_system()
    """Real-world security monitoring system"""
    
    println("\n🔒 SECURITY CAMERA SYSTEM\n")
    
    let camera = initialize_camera(device_id: 0)
    let log = []
    let alerts = []
    
    for i in range(0, 30)  # 30 frames
        let frame = capture_frame_from_camera(camera)
        let faces = detect_faces(frame)
        let objects = detect_objects(frame)
        
        # Check for intruders
        let intruders = 0
        for obj in objects
            if obj["class"] == "person" and obj["confidence"] > 0.8
                intruders = intruders + 1
        
        # Log event
        let event = {
            "timestamp": time_current(),
            "frame": i,
            "faces_detected": len(faces),
            "objects_detected": len(objects),
            "intruders": intruders
        }
        
        log = append(log, event)
        
        # Alert if intruder detected
        if intruders > 0
            let alert = {
                "type": "INTRUDER_ALERT",
                "timestamp": time_current(),
                "count": intruders,
                "frame": frame
            }
            alerts = append(alerts, alert)
            println("🚨 ALERT: " + str(intruders) + " intruder(s) detected!")
        
        println("Frame " + str(i) + ": " + str(len(faces)) + " faces, " + str(len(objects)) + " objects")
    
    # Save log
    write_file(path: "./security_log.json", content: to_json(log))
    
    println("\n📊 Security Summary:")
    println("Total frames: " + str(len(log)))
    println("Alerts triggered: " + str(len(alerts)))
    
    return {"log": log, "alerts": alerts}

fn main()
    security_camera_system()
```

### Example 2: Health & Wellness Monitor

```tombo
use bio_sensors
use audio
use io

fn health_monitor_app()
    """Monitor health with camera, audio, and biometric sensors"""
    
    println("\n❤️  HEALTH & WELLNESS MONITOR\n")
    
    let session = {
        "duration": 60,
        "readings": [],
        "anomalies": [],
        "recommendations": []
    }
    
    for second in range(0, 60)
        # Read all sensors
        let hr = read_heart_rate(nil)
        let o2 = read_blood_oxygen(nil)
        let temp = read_temperature(nil)
        let steps = read_step_count(nil)
        
        let reading = {
            "timestamp": second,
            "heart_rate": hr["value"],
            "o2_saturation": o2["value"],
            "body_temp": temp["value"],
            "steps": steps["value"]
        }
        
        session["readings"] = append(session["readings"], reading)
        
        # Check for anomalies
        if hr["value"] > 120
            session["anomalies"] = append(session["anomalies"], {
                "type": "high_heart_rate",
                "timestamp": second,
                "value": hr["value"]
            })
            println("⚠️  High heart rate: " + str(hr["value"]) + " bpm")
        
        if temp["value"] > 38.0
            session["anomalies"] = append(session["anomalies"], {
                "type": "fever",
                "timestamp": second,
                "value": temp["value"]
            })
            println("🌡️  Fever detected: " + str(temp["value"]) + "°C")
        
        println("HR: " + str(hr["value"]) + " | O2: " + str(o2["value"]) + "% | Temp: " + str(temp["value"]) + "°C")
    
    # Generate recommendations
    let avg_hr = 72
    if avg_hr < 60
        session["recommendations"] = append(session["recommendations"], "Increase daily activity")
    if avg_hr > 90
        session["recommendations"] = append(session["recommendations"], "Reduce stress, practice meditation")
    
    session["recommendations"] = append(session["recommendations"], "Maintain hydration")
    session["recommendations"] = append(session["recommendations"], "Get 8 hours of sleep")
    
    println("\n📋 Recommendations:")
    for rec in session["recommendations"]
        println("• " + rec)
    
    write_file(path: "./health_session.json", content: to_json(session))
    
    return session

fn main()
    health_monitor_app()
```

### Example 3: Voice-Activated Assistant

```tombo
use audio
use io

fn voice_assistant()
    """Voice-activated assistant using microphone"""
    
    println("\n🎙️ VOICE ASSISTANT\n")
    println("Listening for commands...\n")
    
    let commands = []
    let sessions = []
    
    for session_num in range(0, 3)  # 3 listening sessions
        println("Session " + str(session_num + 1) + ": Listening...")
        
        let audio = record_audio(duration_seconds: 5)
        
        # Detect voice activity
        let has_voice = false
        for sample in audio["samples"]
            if sample > 10
                has_voice = true
        
        if has_voice
            println("✓ Voice detected")
            
            # Simulate speech recognition
            let transcribed = recognize_speech(audio)
            
            let command = {
                "session": session_num,
                "text": transcribed,
                "duration": 5,
                "confidence": 0.85
            }
            
            commands = append(commands, command)
            
            # Execute command
            let response = execute_command(transcribed)
            println("Assistant: " + response)
        else
            println("No voice detected")
        
        time_sleep(500)
    
    println("\n📝 Commands Processed: " + str(len(commands)))
    for cmd in commands
        println("• " + cmd["text"])
    
    return commands

fn recognize_speech(audio: Dict) -> String
    return "set alarm for 7am"  # Simulated

fn execute_command(cmd: String) -> String
    if cmd == "set alarm for 7am"
        return "Alarm set for 7:00 AM"
    return "Command received"

fn main()
    voice_assistant()
```

---

## Troubleshooting

### Common Issues & Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| **Camera not opening** | Device in use or not found | Check device ID, close other apps |
| **Permission denied** | App lacks permissions | Grant camera/microphone permissions in OS |
| **Low audio quality** | Poor microphone | Increase gain, reduce noise filter |
| **Lag/Delay** | Processing too slow | Reduce frame size, lower sampling rate |
| **Sensor not detected** | Device not connected | Check USB cable, try different port |
| **Frames missing** | Buffer overflow | Reduce frame resolution or FPS |

### Permission Checklist

✓ **Windows:**
```
Settings → Privacy → Camera → Enable app
Settings → Privacy → Microphone → Enable app
```

✓ **macOS:**
```
System Preferences → Security & Privacy → Camera
System Preferences → Security & Privacy → Microphone
```

✓ **Linux:**
```
sudo usermod -a -G audio,video $USER
```

### Performance Optimization

```tombo
# ✓ GOOD: Optimal settings
let camera = initialize_camera(resolution: "640x480", fps: 30)

# ✗ SLOW: Too high resolution
let camera = initialize_camera(resolution: "4K", fps: 60)

# ✓ GOOD: Reasonable sampling
let audio = record_audio(sample_rate: 16000)  # 16kHz for speech

# ✗ SLOW: Unnecessary high quality
let audio = record_audio(sample_rate: 192000)  # 192kHz
```

---

## Summary

**Tombo Hardware Access Capabilities:**

| Device | Library | Key Functions |
|--------|---------|---|
| 📷 **Camera** | `vision` | `initialize_camera()`, `capture_frame_from_camera()`, `detect_faces()`, `detect_objects()` |
| 🎙️ **Microphone** | `audio` | `record_audio()`, `capture_audio_chunk()`, `detect_speech()`, `apply_reverb()` |
| 📡 **Sensors** | `sensors` | `initialize_sensor()`, `read_sensor()`, `calibrate_sensor()` |
| ❤️ **Biometrics** | `bio_sensors` | `read_heart_rate()`, `read_accelerometer()`, `read_blood_oxygen()` |
| 🌍 **Environment** | `env_sensors` | `read_temperature()`, `read_humidity()`, `read_air_quality()` |
| 🔌 **IoT Devices** | `iot` | Device discovery, connection, control |

**Best Practices:**

1. Always initialize hardware before use
2. Handle permissions properly
3. Use try-catch for errors
4. Process data in real-time when needed
5. Save critical data to files
6. Close devices when done
7. Monitor resource usage

---

**🚀 Start building with hardware in Tombo today!**
