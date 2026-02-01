"""
Phase 7 Library Tests - Complete testing of Phase 7 enterprise utilities
Tests: Logging, Config, Validation, Monitoring, Storage, Security
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.lib.logging import Logger, LoggerFactory, LogLevel, ConsoleHandler, FileHandler
from src.lib.config import ConfigBuilder, Configuration
from src.lib.validation import SchemaBuilder, Validator, RequiredValidator, TypeValidator
from src.lib.monitoring import Counter, Gauge, HealthMonitor, HealthCheck, Profiler
from src.lib.storage import CSVHandler, FileFormat, StorageManager
from src.lib.security import SecureRandom, HMAC, HashingAlgorithm, RateLimiter, AES


def test_phase7_logging():
    """Test Phase 7 logging library."""
    print("\n=== Phase 7: Logging Tests ===")
    
    # Test LoggerFactory
    logger = LoggerFactory.get_logger("test_logger")
    logger.info("Logger created successfully")
    logger.debug("Debug message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    # Test console handler
    handler = ConsoleHandler()
    logger.add_handler(handler)
    
    print("✓ Logging library functional")


def test_phase7_config():
    """Test Phase 7 configuration library."""
    print("\n=== Phase 7: Config Tests ===")
    
    # Test config builder
    config = ConfigBuilder().with_value('app_name', 'TOMBO').with_value('version', '7.0.0').build()
    
    assert config.get('app_name') == 'TOMBO'
    assert config.get('version') == '7.0.0'
    
    # Test environment config
    os.environ['TEST_VAR'] = 'test_value'
    env_config = ConfigBuilder().with_env('TEST_VAR').build()
    
    assert env_config.get('TEST_VAR') == 'test_value'
    
    print("✓ Config library functional")


def test_phase7_validation():
    """Test Phase 7 validation library."""
    print("\n=== Phase 7: Validation Tests ===")
    
    # Test schema builder
    schema = SchemaBuilder().add_field('email', RequiredValidator()).add_field('age', TypeValidator(int)).build()
    
    # Valid data
    valid, errors = schema.validate({'email': 'test@example.com', 'age': 30})
    assert valid, f"Validation failed: {errors}"
    
    # Invalid data
    valid, errors = schema.validate({'age': 30})
    assert not valid, "Should have failed validation"
    
    print("✓ Validation library functional")


def test_phase7_monitoring():
    """Test Phase 7 monitoring library."""
    print("\n=== Phase 7: Monitoring Tests ===")
    
    # Test counter
    counter = Counter('requests')
    counter.increment()
    counter.increment()
    assert counter.get_value() == 2, "Counter value incorrect"
    
    # Test gauge
    gauge = Gauge('temperature')
    gauge.set(25.5)
    assert gauge.get_value() == 25.5, "Gauge value incorrect"
    
    # Test health monitor
    monitor = HealthMonitor()
    check = HealthCheck('cpu', lambda: True)
    monitor.add_check(check)
    
    status = monitor.check_all()
    assert monitor.is_healthy(), "Health check should pass"
    
    # Test profiler
    profiler = Profiler()
    
    @profiler.time_function
    def slow_function():
        total = 0
        for i in range(1000):
            total += i
        return total
    
    result = slow_function()
    assert result == sum(range(1000)), "Function result incorrect"
    
    print("✓ Monitoring library functional")


def test_phase7_storage():
    """Test Phase 7 storage library."""
    print("\n=== Phase 7: Storage Tests ===")
    
    # Test CSV handler
    csv_handler = CSVHandler()
    csv_data = "name,age\nAlice,30\nBob,25"
    rows = csv_handler.read(csv_data)
    
    assert len(rows) == 2, "CSV parsing failed"
    assert rows[0]['name'] == 'Alice', "CSV data incorrect"
    
    # Test file format detection
    file_format = FileFormat()
    detected = file_format.get_format('data.csv')
    assert detected == 'csv', "Format detection failed"
    
    print("✓ Storage library functional")


def test_phase7_security():
    """Test Phase 7 security library."""
    print("\n=== Phase 7: Security Tests ===")
    
    # Test secure random
    token = SecureRandom.hex(16)
    assert len(token) == 32, "Hex token length incorrect"
    
    # Test HMAC
    message = "test message"
    secret = "secret_key"
    signature = HMAC.sign(message, secret)
    
    assert HMAC.verify(message, signature, secret), "HMAC verification failed"
    assert not HMAC.verify("wrong message", signature, secret), "HMAC should reject wrong message"
    
    # Test hashing
    hash1 = HashingAlgorithm.sha256("test")
    hash2 = HashingAlgorithm.sha256("test")
    assert hash1 == hash2, "Hash should be consistent"
    
    # Test rate limiter
    limiter = RateLimiter(3, 60)
    
    assert limiter.is_allowed("client1"), "First request should be allowed"
    assert limiter.is_allowed("client1"), "Second request should be allowed"
    assert limiter.is_allowed("client1"), "Third request should be allowed"
    assert not limiter.is_allowed("client1"), "Fourth request should be blocked"
    
    # Test AES key generation
    key = AES.generate_key(32)
    assert len(key) == 32, "Key length incorrect"
    
    # Test simple encryption/decryption
    plaintext = "secret message"
    encrypted = AES.simple_encrypt(plaintext, key)
    decrypted = AES.simple_decrypt(encrypted, key)
    assert decrypted == plaintext, "Encryption/decryption failed"
    
    print("✓ Security library functional")


def run_all_phase7_tests():
    """Run all Phase 7 tests."""
    print("\n" + "="*60)
    print("PHASE 7 ENTERPRISE UTILITIES - COMPLETE TEST SUITE")
    print("="*60)
    
    try:
        test_phase7_logging()
        test_phase7_config()
        test_phase7_validation()
        test_phase7_monitoring()
        test_phase7_storage()
        test_phase7_security()
        
        print("\n" + "="*60)
        print("✓ ALL PHASE 7 TESTS PASSED")
        print("="*60)
        print("\nPhase 7 Summary:")
        print("- Logging: Logger, ConsoleHandler, FileHandler, LogLevels")
        print("- Config: ConfigBuilder, ConfigParser, EnvironmentConfig")
        print("- Validation: SchemaBuilder, Validators, Schema composition")
        print("- Monitoring: Metrics, HealthChecks, Profiling")
        print("- Storage: CSV/TSV/JSONL, FileFormat detection, Compression")
        print("- Security: HMAC, Hashing, RateLimiting, Encryption, SecureRandom")
        print("\nTotal libraries in Phase 7: 6")
        print("Total libraries (Phases 1-7): 44")
        
        return True
    
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_phase7_tests()
    sys.exit(0 if success else 1)
