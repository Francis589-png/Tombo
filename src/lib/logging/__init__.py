"""
TOMBO Logging Library - Application logging with multiple levels and handlers
File, console, and structured logging with filtering and formatting.
"""

import time
import os
from typing import Dict, List, Optional, Callable


class LogLevel:
    """Log level constants."""
    
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    
    NAMES = {
        10: "DEBUG",
        20: "INFO",
        30: "WARNING",
        40: "ERROR",
        50: "CRITICAL"
    }


class LogRecord:
    """Single log record."""
    
    def __init__(self, name: str, level: int, message: str, **kwargs):
        """Initialize log record.
        
        Args:
            name: Logger name
            level: Log level
            message: Log message
            **kwargs: Extra fields
        """
        self.name = name
        self.level = level
        self.level_name = LogLevel.NAMES.get(level, "UNKNOWN")
        self.message = message
        self.timestamp = time.time()
        self.extra = kwargs
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "level": self.level,
            "level_name": self.level_name,
            "message": self.message,
            "timestamp": self.timestamp,
            "extra": self.extra
        }
    
    def format(self, fmt: str = None) -> str:
        """Format record.
        
        Args:
            fmt: Format string (%(levelname)s %(message)s etc)
            
        Returns:
            Formatted message
        """
        if not fmt:
            fmt = "[%(levelname)s] %(message)s"
        
        formatted = fmt
        formatted = formatted.replace("%(levelname)s", self.level_name)
        formatted = formatted.replace("%(message)s", self.message)
        formatted = formatted.replace("%(name)s", self.name)
        formatted = formatted.replace("%(timestamp)s", str(self.timestamp))
        
        for key, val in self.extra.items():
            formatted = formatted.replace(f"%({key})s", str(val))
        
        return formatted


class Handler:
    """Base log handler."""
    
    def __init__(self, level: int = LogLevel.DEBUG, fmt: str = None):
        """Initialize handler.
        
        Args:
            level: Minimum log level
            fmt: Log format string
        """
        self.level = level
        self.format_str = fmt or "[%(levelname)s] %(message)s"
    
    def handle(self, record: LogRecord):
        """Handle log record."""
        if record.level >= self.level:
            self.emit(record)
    
    def emit(self, record: LogRecord):
        """Emit record (override in subclass)."""
        raise NotImplementedError


class ConsoleHandler(Handler):
    """Log to console."""
    
    def emit(self, record: LogRecord):
        """Print to console."""
        formatted = record.format(self.format_str)
        print(formatted)


class FileHandler(Handler):
    """Log to file."""
    
    def __init__(self, filename: str, level: int = LogLevel.DEBUG, fmt: str = None):
        """Initialize file handler.
        
        Args:
            filename: Log file path
            level: Minimum log level
            fmt: Log format
        """
        super().__init__(level, fmt)
        self.filename = filename
    
    def emit(self, record: LogRecord):
        """Write to file."""
        formatted = record.format(self.format_str)
        
        try:
            with open(self.filename, 'a') as f:
                f.write(formatted + '\n')
        except Exception as e:
            print(f"Error writing to log file: {e}")


class RotatingFileHandler(Handler):
    """Log to file with rotation."""
    
    def __init__(self, filename: str, max_bytes: int = 10485760, 
                 backup_count: int = 5, level: int = LogLevel.DEBUG, fmt: str = None):
        """Initialize rotating file handler.
        
        Args:
            filename: Log file path
            max_bytes: Max file size before rotation
            backup_count: Number of backup files
            level: Minimum log level
            fmt: Log format
        """
        super().__init__(level, fmt)
        self.filename = filename
        self.max_bytes = max_bytes
        self.backup_count = backup_count
    
    def emit(self, record: LogRecord):
        """Write to file with rotation."""
        formatted = record.format(self.format_str)
        
        try:
            # Check if rotation needed
            if os.path.exists(self.filename):
                if os.path.getsize(self.filename) >= self.max_bytes:
                    self._rotate()
            
            with open(self.filename, 'a') as f:
                f.write(formatted + '\n')
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def _rotate(self):
        """Rotate log files."""
        for i in range(self.backup_count - 1, 0, -1):
            src = f"{self.filename}.{i}"
            dst = f"{self.filename}.{i + 1}"
            
            if os.path.exists(src):
                if os.path.exists(dst):
                    os.remove(dst)
                os.rename(src, dst)
        
        if os.path.exists(self.filename):
            os.rename(self.filename, f"{self.filename}.1")


class Logger:
    """Application logger."""
    
    def __init__(self, name: str, level: int = LogLevel.DEBUG):
        """Initialize logger.
        
        Args:
            name: Logger name
            level: Logger level
        """
        self.name = name
        self.level = level
        self.handlers: List[Handler] = []
        self.filters: List[Callable] = []
    
    def add_handler(self, handler: Handler):
        """Add handler."""
        self.handlers.append(handler)
        return self
    
    def add_filter(self, filter_func: Callable[[LogRecord], bool]):
        """Add filter."""
        self.filters.append(filter_func)
        return self
    
    def _log(self, level: int, message: str, **kwargs):
        """Internal log method."""
        if level < self.level:
            return
        
        record = LogRecord(self.name, level, message, **kwargs)
        
        # Apply filters
        for filter_func in self.filters:
            if not filter_func(record):
                return
        
        # Emit to handlers
        for handler in self.handlers:
            handler.handle(record)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self._log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self._log(LogLevel.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self._log(LogLevel.CRITICAL, message, **kwargs)


class LoggerFactory:
    """Create and manage loggers."""
    
    _loggers: Dict[str, Logger] = {}
    _default_level = LogLevel.INFO
    _default_handlers: List[Handler] = []
    
    @classmethod
    def set_default_level(cls, level: int):
        """Set default log level."""
        cls._default_level = level
    
    @classmethod
    def add_default_handler(cls, handler: Handler):
        """Add handler to all loggers."""
        cls._default_handlers.append(handler)
        
        for logger in cls._loggers.values():
            logger.add_handler(handler)
    
    @classmethod
    def get_logger(cls, name: str) -> Logger:
        """Get or create logger."""
        if name not in cls._loggers:
            logger = Logger(name, cls._default_level)
            
            for handler in cls._default_handlers:
                logger.add_handler(handler)
            
            cls._loggers[name] = logger
        
        return cls._loggers[name]


# Global logger instance
_root_logger = LoggerFactory.get_logger("root")


def get_logger(name: str) -> Logger:
    """Get logger by name."""
    return LoggerFactory.get_logger(name)


def configure_logging(level: int, console: bool = True, file: str = None,
                     fmt: str = None):
    """Configure logging globally.
    
    Args:
        level: Log level
        console: Log to console
        file: Log to file
        fmt: Log format
    """
    LoggerFactory.set_default_level(level)
    
    if console:
        handler = ConsoleHandler(level, fmt)
        LoggerFactory.add_default_handler(handler)
    
    if file:
        handler = FileHandler(file, level, fmt)
        LoggerFactory.add_default_handler(handler)
