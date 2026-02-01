# Quick Reference: Hardware Access in Tombo

**Fast lookup guide for accessing hardware devices**

---

## 📷 CAMERA

### Initialize Camera
```tombo
use vision

let camera = initialize_camera(device_id: 0)
```

### Capture Frame
```tombo
let frame = capture_frame_from_camera(camera)
```

### Face Detection
```tombo
let faces = detect_faces(frame)
```

### Object Detection
```tombo
let objects = detect_objects(frame)
```

### Save Image
```tombo
save_image(frame, path: "output.jpg")
```

---

## 🎙️ MICROPHONE

### Record Audio
```tombo
use audio

let recording = record_audio(duration_seconds: 5)
```

### Save Recording
```tombo
save_audio(recording, filename: "voice.wav")
```

### Detect Speech
```tombo
let has_speech = detect_speech(recording)
```

### Speech Recognition
```tombo
let text = recognize_speech(recording)
```

### Apply Effects
```tombo
let reverb = tombo_apply_reverb(recording, decay: 0.5)
```

---

## ❤️ BIOMETRIC SENSORS

### Heart Rate
```tombo
use bio_sensors

let hr = read_heart_rate(sensor)
println("HR: " + str(hr["value"]) + " bpm")
```

### Blood Oxygen
```tombo
let o2 = read_blood_oxygen(sensor)
println("O2: " + str(o2["value"]) + "%")
```

### Body Temperature
```tombo
let temp = read_temperature(sensor)
println("Temp: " + str(temp["value"]) + "°C")
```

### Blood Pressure
```tombo
let bp = read_blood_pressure(sensor)
println("BP: " + str(bp["systolic"]) + "/" + str(bp["diastolic"]))
```

### ECG (10 sec)
```tombo
let ecg = read_ecg(sensor, duration: 10)
```

### Step Counter
```tombo
let steps = read_step_count(sensor)
```

### Accelerometer
```tombo
let accel = read_accelerometer(sensor)
println("X: " + str(accel["x"]))
```

### Gyroscope
```tombo
let gyro = read_gyroscope(sensor)
```

---

## 🌍 ENVIRONMENTAL SENSORS

### Temperature & Humidity
```tombo
use env_sensors

let temp = read_temperature(sensor)
let humidity = read_humidity(sensor)
```

### Air Quality
```tombo
let air = read_air_quality(sensor)
println("AQI: " + str(air["aqi"]))
```

### CO2 Level
```tombo
let co2 = read_co2(sensor)
```

### Pressure
```tombo
let pressure = read_pressure(sensor)
```

---

## 📡 GENERAL SENSORS

### Initialize Sensor
```tombo
use sensors

let sensor = initialize_sensor(sensor_type: "temperature", port: "COM3")
```

### Read Sensor
```tombo
let value = read_sensor(sensor)
```

### Configure Sensor
```tombo
configure_sensor(sensor, config: {"range": [0, 100], "precision": 0.1})
```

### Calibrate
```tombo
calibrate_sensor(sensor, reference_values: [20.0, 30.0])
```

### Stream Recording
```tombo
record_sensor_stream(sensor, filename: "data.log", duration: 60)
```

### Detect Anomalies
```tombo
let anomalies = detect_sensor_anomalies(sensor, threshold: 3.0)
```

---

## 🔌 IOT DEVICE CONTROL

### Discover Devices
```tombo
use iot

let devices = discover_devices(network: "192.168.1.0/24")
```

### Connect Device
```tombo
let device = connect_device(ip: "192.168.1.100", port: 8080)
```

### Send Command
```tombo
send_command(device, command: "ON")
```

### Get Status
```tombo
let status = get_device_status(device)
```

---

## ⚙️ MULTI-DEVICE USAGE

### Read Multiple Sensors
```tombo
let sensors = [sensor1, sensor2, sensor3]
let values = read_sensor_multiple(sensors)
```

### Synchronize Sensors
```tombo
synchronize_sensors(sensors)
```

### Sensor Fusion
```tombo
let fused = fuse_sensor_data(sensors)
```

### Stream to Cloud
```tombo
stream_to_cloud(sensor, endpoint: "api.example.com/data", api_key: "key123")
```

---

## 📊 DATA COLLECTION PATTERN

```tombo
use vision
use audio
use bio_sensors
use io
use json

fn collect_all_data() -> Dict
    let data = {
        "timestamp": time_current(),
        "camera": capture_frame_from_camera(camera),
        "audio": record_audio(duration_seconds: 5),
        "heart_rate": read_heart_rate(sensor),
        "temperature": read_temperature(sensor)
    }
    
    # Save to file
    write_file(path: "data.json", content: to_json(data))
    
    return data

fn main()
    collect_all_data()
```

---

## 🚨 ERROR HANDLING PATTERN

```tombo
fn safe_sensor_read(sensor: Dict) -> Dict
    let result = {
        "success": false,
        "value": nil,
        "error": nil
    }
    
    try
        let reading = read_sensor(sensor)
        result["success"] = true
        result["value"] = reading
    catch error
        result["error"] = error
        println("❌ Error: " + error)
    
    return result
```

---

## ⚡ PERFORMANCE TIPS

✓ **Use lower resolution for real-time processing**
```tombo
let camera = initialize_camera(resolution: "640x480", fps: 30)
```

✓ **Buffer sensor data**
```tombo
enable_sensor_buffering(sensor, buffer_size: 1000)
let data = get_sensor_buffer(sensor)
```

✓ **Filter noisy data**
```tombo
enable_sensor_filtering(sensor, filter_type: "moving_average", window: 5)
```

✓ **Parallel processing**
```tombo
synchronize_sensors([sensor1, sensor2])
```

---

## 🔧 DEVICE TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Camera won't open | Check device ID, close other apps |
| Permission denied | Grant camera/mic permissions in OS |
| No sensor data | Verify USB cable, check port |
| Lag/delay | Reduce resolution, increase buffer |
| Audio crackling | Lower sample rate, check mic level |

---

## 📝 COMMON PATTERNS

### Real-Time Loop
```tombo
for i in range(0, 100)
    let frame = capture_frame_from_camera(camera)
    let data = process(frame)
    println("Frame " + str(i) + ": done")
    time_sleep(33)  # ~30fps
```

### Continuous Recording
```tombo
let recording = record_audio(duration_seconds: 300)  # 5 minutes
save_audio(recording, filename: "session.wav")
```

### Monitoring Loop
```tombo
let readings = []
for i in range(0, 1000)
    let value = read_sensor(sensor)
    readings = append(readings, value)
    if value > threshold
        println("⚠️  Alert!")
```

### Data Logging
```tombo
let session = []
for i in range(0, 100)
    let reading = read_all_sensors()
    session = append(session, reading)
write_file(path: "log.json", content: to_json(session))
```

---

**More examples:** See `docs/HARDWARE_ACCESS_GUIDE.md` and `examples/iot_dashboard_project.to`
