"""
TOMBO System Domain - System, logging, configuration, and monitoring
Provides logging, config management, monitoring, and performance tracking
"""

# Import Phase 7 system libraries
from tombo.lib.logging import Logger, LoggerFactory, LogLevel, Handler, ConsoleHandler, FileHandler, RotatingFileHandler, LogRecord
from tombo.lib.config import Configuration, ConfigParser, ConfigBuilder, EnvironmentConfig
from tombo.lib.monitoring import Metric, Counter, Gauge, Histogram, Timer, MetricsRegistry, HealthCheck, HealthMonitor, Profiler
from tombo.lib.validation import Schema, SchemaBuilder, Validator, RequiredValidator, TypeValidator, EmailValidator, URLValidator

# Export main classes
__all__ = [
    'Logger', 'LoggerFactory', 'LogLevel', 'ConsoleHandler', 'FileHandler', 'RotatingFileHandler',
    'Configuration', 'ConfigParser', 'ConfigBuilder',
    'Metric', 'Counter', 'Gauge', 'Histogram', 'Timer', 'MetricsRegistry',
    'HealthCheck', 'HealthMonitor', 'Profiler',
    'Schema', 'SchemaBuilder', 'Validator', 'RequiredValidator', 'TypeValidator'
]

# Domain metadata
DOMAIN_NAME = 'system'
DOMAIN_LIBRARIES = [
    'logging',
    'config', 
    'monitoring',
    'validation'
]
DOMAIN_VERSION = '7.0.0'
