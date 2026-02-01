#!/usr/bin/env python3
"""Test new computer vision and sensor libraries"""

import sys
import unittest
from src.core.interpreter import Interpreter


class TestNewLibraries(unittest.TestCase):
    """Test computer vision and sensor libraries"""

    def setUp(self):
        self.interp = Interpreter()

    def test_vision_functions_available(self):
        """Test that vision functions are available"""
        functions = [
            'create_image', 'load_image', 'save_image', 'resize_image',
            'convert_to_grayscale', 'detect_faces', 'detect_objects',
            'classify_image', 'segment_image', 'estimate_depth',
        ]
        for fn_name in functions:
            fn = self.interp.global_env.get(fn_name)
            self.assertIsNotNone(fn, f"Vision function {fn_name} not available")
            self.assertTrue(callable(fn), f"{fn_name} is not callable")

    def test_sensors_functions_available(self):
        """Test that sensor functions are available"""
        functions = [
            'initialize_sensor', 'read_sensor', 'configure_sensor',
            'get_sensor_status', 'calibrate_sensor', 'record_sensor_stream',
            'fuse_sensor_data', 'detect_sensor_anomalies',
        ]
        for fn_name in functions:
            fn = self.interp.global_env.get(fn_name)
            self.assertIsNotNone(fn, f"Sensor function {fn_name} not available")
            self.assertTrue(callable(fn), f"{fn_name} is not callable")

    def test_env_sensors_functions_available(self):
        """Test that environmental sensor functions are available"""
        functions = [
            'initialize_temperature_sensor', 'read_temperature', 'read_humidity',
            'read_pressure', 'read_air_quality', 'read_co2',
            'get_weather_forecast', 'calculate_dew_point',
        ]
        for fn_name in functions:
            fn = self.interp.global_env.get(fn_name)
            self.assertIsNotNone(fn, f"Env sensor function {fn_name} not available")
            self.assertTrue(callable(fn), f"{fn_name} is not callable")

    def test_bio_sensors_functions_available(self):
        """Test that biometric sensor functions are available"""
        functions = [
            'initialize_heart_rate_monitor', 'read_heart_rate', 'read_blood_oxygen',
            'read_blood_pressure', 'read_sleep_data', 'detect_heart_arrhythmia',
            'get_health_score', 'set_health_goal',
        ]
        for fn_name in functions:
            fn = self.interp.global_env.get(fn_name)
            self.assertIsNotNone(fn, f"Bio sensor function {fn_name} not available")
            self.assertTrue(callable(fn), f"{fn_name} is not callable")

    def test_vision_create_image(self):
        """Test creating an image"""
        fn = self.interp.global_env.get('create_image')
        result = fn(800, 600)
        self.assertEqual(result['type'], 'image')
        self.assertEqual(result['width'], 800)
        self.assertEqual(result['height'], 600)

    def test_vision_image_operations(self):
        """Test image transformation operations"""
        create_img = self.interp.global_env.get('create_image')
        resize_img = self.interp.global_env.get('resize_image')

        img = create_img(800, 600)
        result = resize_img(img, 400, 300, "bilinear")

        self.assertEqual(result['width'], 400)
        self.assertEqual(result['height'], 300)
        self.assertTrue(result['resized'])

    def test_sensor_initialization(self):
        """Test sensor initialization"""
        init_fn = self.interp.global_env.get('initialize_sensor')
        result = init_fn('temperature', '/dev/ttyUSB0')

        self.assertEqual(result['type'], 'sensor')
        self.assertTrue(result['initialized'])

    def test_env_sensor_reading(self):
        """Test environmental sensor reading"""
        read_temp = self.interp.global_env.get('read_temperature')
        result = read_temp({})

        self.assertEqual(result['type'], 'temperature')
        self.assertIn('value', result)
        self.assertEqual(result['unit'], 'celsius')

    def test_bio_sensor_reading(self):
        """Test biometric sensor reading"""
        read_hr = self.interp.global_env.get('read_heart_rate')
        result = read_hr({})

        self.assertEqual(result['type'], 'heart_rate')
        self.assertIn('value', result)
        self.assertEqual(result['unit'], 'bpm')

    def test_total_function_count(self):
        """Verify total function count"""
        count = 0
        for name in self.interp.global_env.store:
            obj = self.interp.global_env.store[name]
            if callable(obj):
                count += 1

        # Should have at least core functions + new libraries
        # Estimate: 308 (stdlib) + 257 (new) = 565+
        self.assertGreater(count, 500, f"Expected 500+ functions, got {count}")
        print(f"\nTotal callable functions loaded: {count}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
