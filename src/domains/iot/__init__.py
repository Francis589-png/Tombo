"""
Tombo IoT Domain - Internet of Things
Provides sensors, actuators, protocols, device management
"""

class Sensor:
    def __init__(self, sensor_id='', sensor_type='', pin=0):
        self.id = sensor_id
        self.type = sensor_type
        self.pin = pin
        self.value = 0
        self.unit = ''
        self.status = 'inactive'
    
    def read(self):
        """Read sensor value."""
        return self.value
    
    def calibrate(self):
        """Calibrate sensor."""
        return True
    
    def set_status(self, status):
        """Set sensor status."""
        self.status = status
        return self

class Actuator:
    def __init__(self, actuator_id='', actuator_type='', pin=0):
        self.id = actuator_id
        self.type = actuator_type
        self.pin = pin
        self.value = 0
        self.status = 'off'
    
    def activate(self):
        """Activate actuator."""
        self.status = 'on'
        return True
    
    def deactivate(self):
        """Deactivate actuator."""
        self.status = 'off'
        return True
    
    def set_value(self, value):
        """Set actuator value."""
        self.value = value
        return True

class Device:
    def __init__(self, device_id='', device_type=''):
        self.id = device_id
        self.type = device_type
        self.sensors = {}
        self.actuators = {}
        self.connected = True
        self.properties = {}
    
    def add_sensor(self, sensor):
        """Add sensor to device."""
        self.sensors[sensor.id] = sensor
        return self
    
    def add_actuator(self, actuator):
        """Add actuator to device."""
        self.actuators[actuator.id] = actuator
        return self
    
    def get_sensor(self, sensor_id):
        """Get sensor by ID."""
        return self.sensors.get(sensor_id)
    
    def get_actuator(self, actuator_id):
        """Get actuator by ID."""
        return self.actuators.get(actuator_id)
    
    def read_all_sensors(self):
        """Read all sensors."""
        return {sid: sensor.read() for sid, sensor in self.sensors.items()}
    
    def control_all_actuators(self, values):
        """Control all actuators."""
        for aid, value in values.items():
            if aid in self.actuators:
                self.actuators[aid].set_value(value)
        return True

class Gateway:
    def __init__(self, gateway_id=''):
        self.id = gateway_id
        self.devices = {}
        self.connected_devices = 0
    
    def register_device(self, device):
        """Register device with gateway."""
        self.devices[device.id] = device
        self.connected_devices += 1
        return True
    
    def unregister_device(self, device_id):
        """Unregister device."""
        if device_id in self.devices:
            del self.devices[device_id]
            self.connected_devices -= 1
        return True
    
    def get_device(self, device_id):
        """Get device by ID."""
        return self.devices.get(device_id)
    
    def list_devices(self):
        """List all devices."""
        return list(self.devices.keys())

# Sensor Operations
def tombo_create_sensor(sensor_id, sensor_type, pin):
    """Create sensor."""
    return Sensor(sensor_id, sensor_type, pin)

def tombo_read_sensor(sensor):
    """Read sensor value."""
    return sensor.read()

def tombo_calibrate_sensor(sensor):
    """Calibrate sensor."""
    return sensor.calibrate()

def tombo_temperature_sensor(pin):
    """Create temperature sensor."""
    sensor = Sensor(f'temp_{pin}', 'temperature', pin)
    sensor.unit = '°C'
    return sensor

def tombo_humidity_sensor(pin):
    """Create humidity sensor."""
    sensor = Sensor(f'humidity_{pin}', 'humidity', pin)
    sensor.unit = '%'
    return sensor

def tombo_pressure_sensor(pin):
    """Create pressure sensor."""
    sensor = Sensor(f'pressure_{pin}', 'pressure', pin)
    sensor.unit = 'hPa'
    return sensor

def tombo_motion_sensor(pin):
    """Create motion sensor."""
    return Sensor(f'motion_{pin}', 'motion', pin)

def tombo_light_sensor(pin):
    """Create light sensor."""
    sensor = Sensor(f'light_{pin}', 'light', pin)
    sensor.unit = 'lux'
    return sensor

def tombo_gas_sensor(pin):
    """Create gas sensor."""
    sensor = Sensor(f'gas_{pin}', 'gas', pin)
    sensor.unit = 'ppm'
    return sensor

# Actuator Operations
def tombo_create_actuator(actuator_id, actuator_type, pin):
    """Create actuator."""
    return Actuator(actuator_id, actuator_type, pin)

def tombo_activate_actuator(actuator):
    """Activate actuator."""
    return actuator.activate()

def tombo_deactivate_actuator(actuator):
    """Deactivate actuator."""
    return actuator.deactivate()

def tombo_led(pin):
    """Create LED actuator."""
    return Actuator(f'led_{pin}', 'led', pin)

def tombo_motor(pin):
    """Create motor actuator."""
    return Actuator(f'motor_{pin}', 'motor', pin)

def tombo_relay(pin):
    """Create relay actuator."""
    return Actuator(f'relay_{pin}', 'relay', pin)

def tombo_servo(pin):
    """Create servo actuator."""
    return Actuator(f'servo_{pin}', 'servo', pin)

# Device Management
def tombo_create_device(device_id, device_type):
    """Create IoT device."""
    return Device(device_id, device_type)

def tombo_create_gateway(gateway_id=''):
    """Create IoT gateway."""
    return Gateway(gateway_id)

# Protocols
def tombo_mqtt_publish(topic, message, qos=0):
    """Publish MQTT message."""
    return {'topic': topic, 'message': message, 'qos': qos, 'published': True}

def tombo_mqtt_subscribe(topic, callback):
    """Subscribe to MQTT topic."""
    return {'topic': topic, 'callback': callback, 'subscribed': True}

def tombo_coap_request(resource, method='GET', payload=''):
    """CoAP request."""
    return {'resource': resource, 'method': method, 'payload': payload}

def tombo_http_request(url, method='GET', data=''):
    """HTTP request."""
    return {'url': url, 'method': method, 'data': data, 'status': 200}

def tombo_bluetooth_send(device, data):
    """Send data over Bluetooth."""
    return True

def tombo_zigbee_send(device, data):
    """Send data over ZigBee."""
    return True

def tombo_lora_send(data, frequency=868):
    """Send data over LoRa."""
    return True

# Data Management
def tombo_store_sensor_data(database, device_id, sensor_id, value, timestamp=None):
    """Store sensor data."""
    return {'stored': True, 'device': device_id, 'sensor': sensor_id}

def tombo_query_sensor_data(database, device_id, sensor_id, time_range=None):
    """Query sensor data."""
    return []

def tombo_aggregate_sensor_data(data, aggregation='mean'):
    """Aggregate sensor data."""
    if not data:
        return 0
    if aggregation == 'mean':
        return sum(data) / len(data)
    elif aggregation == 'sum':
        return sum(data)
    elif aggregation == 'min':
        return min(data)
    elif aggregation == 'max':
        return max(data)
    return 0

# Rules & Automation
class Rule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action
        self.enabled = True
    
    def evaluate(self, context):
        """Evaluate rule condition."""
        return self.condition(context)
    
    def execute(self):
        """Execute rule action."""
        return self.action()

def tombo_create_rule(condition, action):
    """Create automation rule."""
    return Rule(condition, action)

def tombo_enable_rule(rule):
    """Enable rule."""
    rule.enabled = True
    return rule

def tombo_disable_rule(rule):
    """Disable rule."""
    rule.enabled = False
    return rule

# Alerts & Notifications
def tombo_create_alert(alert_id, threshold, comparison):
    """Create alert."""
    return {'id': alert_id, 'threshold': threshold, 'comparison': comparison}

def tombo_check_alert(sensor_value, alert):
    """Check if alert triggered."""
    threshold = alert['threshold']
    comparison = alert['comparison']
    if comparison == 'gt':
        return sensor_value > threshold
    elif comparison == 'lt':
        return sensor_value < threshold
    elif comparison == 'eq':
        return sensor_value == threshold
    return False

def tombo_send_alert(alert_id, message):
    """Send alert notification."""
    return {'alert': alert_id, 'message': message, 'sent': True}

# Power Management
def tombo_get_power_status(device):
    """Get device power status."""
    return {'battery': 85, 'charging': False}

def tombo_set_power_mode(device, mode='normal'):
    """Set device power mode."""
    return True

def tombo_sleep_device(device, duration):
    """Put device to sleep."""
    return True

def tombo_wake_device(device):
    """Wake device from sleep."""
    return True

# Firmware Management
def tombo_check_firmware_update(device):
    """Check for firmware update."""
    return {'available': False, 'version': '1.0.0'}

def tombo_update_firmware(device, firmware_path):
    """Update device firmware."""
    return True

def tombo_rollback_firmware(device, version):
    """Rollback to previous firmware."""
    return True

def register(env):
    """Register IoT domain."""
    env.set('Sensor', Sensor)
    env.set('Actuator', Actuator)
    env.set('Device', Device)
    env.set('Gateway', Gateway)
    env.set('Rule', Rule)
    
    functions = {
        'create_sensor': tombo_create_sensor,
        'read_sensor': tombo_read_sensor,
        'calibrate_sensor': tombo_calibrate_sensor,
        'temperature_sensor': tombo_temperature_sensor,
        'humidity_sensor': tombo_humidity_sensor,
        'pressure_sensor': tombo_pressure_sensor,
        'motion_sensor': tombo_motion_sensor,
        'light_sensor': tombo_light_sensor,
        'gas_sensor': tombo_gas_sensor,
        'create_actuator': tombo_create_actuator,
        'activate_actuator': tombo_activate_actuator,
        'deactivate_actuator': tombo_deactivate_actuator,
        'led': tombo_led,
        'motor': tombo_motor,
        'relay': tombo_relay,
        'servo': tombo_servo,
        'create_device': tombo_create_device,
        'create_gateway': tombo_create_gateway,
        'mqtt_publish': tombo_mqtt_publish,
        'mqtt_subscribe': tombo_mqtt_subscribe,
        'coap_request': tombo_coap_request,
        'http_request': tombo_http_request,
        'bluetooth_send': tombo_bluetooth_send,
        'zigbee_send': tombo_zigbee_send,
        'lora_send': tombo_lora_send,
        'store_sensor_data': tombo_store_sensor_data,
        'query_sensor_data': tombo_query_sensor_data,
        'aggregate_sensor_data': tombo_aggregate_sensor_data,
        'create_rule': tombo_create_rule,
        'enable_rule': tombo_enable_rule,
        'disable_rule': tombo_disable_rule,
        'create_alert': tombo_create_alert,
        'check_alert': tombo_check_alert,
        'send_alert': tombo_send_alert,
        'get_power_status': tombo_get_power_status,
        'set_power_mode': tombo_set_power_mode,
        'sleep_device': tombo_sleep_device,
        'wake_device': tombo_wake_device,
        'check_firmware_update': tombo_check_firmware_update,
        'update_firmware': tombo_update_firmware,
        'rollback_firmware': tombo_rollback_firmware,
    }
    for name, func in functions.items():
        env.set(name, func)

provides = ['iot']
