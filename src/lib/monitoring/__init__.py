"""
TOMBO Monitoring Library - Performance metrics and health monitoring
Counters, gauges, histograms, and health checks.
"""

import time
from typing import Dict, List, Any, Callable, Optional


class Metric:
    """Base metric."""
    
    def __init__(self, name: str, description: str = ""):
        """Initialize metric.
        
        Args:
            name: Metric name
            description: Metric description
        """
        self.name = name
        self.description = description
        self.created_at = time.time()
    
    def get_value(self) -> Any:
        """Get metric value."""
        raise NotImplementedError


class Counter(Metric):
    """Counter metric (monotonically increasing)."""
    
    def __init__(self, name: str, description: str = ""):
        """Initialize counter."""
        super().__init__(name, description)
        self.value = 0
    
    def increment(self, amount: int = 1):
        """Increment counter.
        
        Args:
            amount: Amount to increment
        """
        self.value += amount
    
    def get_value(self) -> int:
        """Get counter value."""
        return self.value


class Gauge(Metric):
    """Gauge metric (can go up or down)."""
    
    def __init__(self, name: str, description: str = ""):
        """Initialize gauge."""
        super().__init__(name, description)
        self.value = 0
    
    def set(self, value: float):
        """Set gauge value.
        
        Args:
            value: Value to set
        """
        self.value = value
    
    def increment(self, amount: float = 1):
        """Increment gauge."""
        self.value += amount
    
    def decrement(self, amount: float = 1):
        """Decrement gauge."""
        self.value -= amount
    
    def get_value(self) -> float:
        """Get gauge value."""
        return self.value


class Histogram(Metric):
    """Histogram metric (distribution of values)."""
    
    def __init__(self, name: str, buckets: List[float] = None, description: str = ""):
        """Initialize histogram.
        
        Args:
            name: Metric name
            buckets: Histogram buckets
            description: Description
        """
        super().__init__(name, description)
        self.buckets = buckets or [1, 5, 10, 50, 100, 500, 1000]
        self.values: List[float] = []
    
    def observe(self, value: float):
        """Record observation.
        
        Args:
            value: Value to record
        """
        self.values.append(value)
    
    def get_value(self) -> Dict:
        """Get histogram statistics."""
        if not self.values:
            return {
                "count": 0,
                "sum": 0,
                "mean": 0,
                "min": 0,
                "max": 0,
                "percentiles": {}
            }
        
        sorted_values = sorted(self.values)
        
        return {
            "count": len(self.values),
            "sum": sum(self.values),
            "mean": sum(self.values) / len(self.values),
            "min": sorted_values[0],
            "max": sorted_values[-1],
            "percentiles": {
                "p50": sorted_values[len(sorted_values) // 2],
                "p95": sorted_values[int(len(sorted_values) * 0.95)],
                "p99": sorted_values[int(len(sorted_values) * 0.99)]
            }
        }


class Timer(Metric):
    """Timer metric (measures duration)."""
    
    def __init__(self, name: str, description: str = ""):
        """Initialize timer."""
        super().__init__(name, description)
        self.durations: List[float] = []
        self.start_time = None
    
    def start(self):
        """Start timer."""
        self.start_time = time.time()
    
    def stop(self):
        """Stop timer and record duration."""
        if self.start_time:
            duration = time.time() - self.start_time
            self.durations.append(duration)
            self.start_time = None
            return duration
        return 0
    
    def get_value(self) -> Dict:
        """Get timer statistics."""
        if not self.durations:
            return {
                "count": 0,
                "total": 0,
                "mean": 0,
                "min": 0,
                "max": 0
            }
        
        return {
            "count": len(self.durations),
            "total": sum(self.durations),
            "mean": sum(self.durations) / len(self.durations),
            "min": min(self.durations),
            "max": max(self.durations)
        }


class MetricsRegistry:
    """Registry for metrics."""
    
    def __init__(self):
        """Initialize registry."""
        self.metrics: Dict[str, Metric] = {}
    
    def counter(self, name: str, description: str = "") -> Counter:
        """Create counter metric."""
        metric = Counter(name, description)
        self.metrics[name] = metric
        return metric
    
    def gauge(self, name: str, description: str = "") -> Gauge:
        """Create gauge metric."""
        metric = Gauge(name, description)
        self.metrics[name] = metric
        return metric
    
    def histogram(self, name: str, buckets: List[float] = None,
                  description: str = "") -> Histogram:
        """Create histogram metric."""
        metric = Histogram(name, buckets, description)
        self.metrics[name] = metric
        return metric
    
    def timer(self, name: str, description: str = "") -> Timer:
        """Create timer metric."""
        metric = Timer(name, description)
        self.metrics[name] = metric
        return metric
    
    def get(self, name: str) -> Optional[Metric]:
        """Get metric by name."""
        return self.metrics.get(name)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all metrics."""
        return {
            name: metric.get_value()
            for name, metric in self.metrics.items()
        }


class HealthCheck:
    """Health check probe."""
    
    def __init__(self, name: str, check_func: Callable[[], bool]):
        """Initialize health check.
        
        Args:
            name: Check name
            check_func: Function that returns True if healthy
        """
        self.name = name
        self.check_func = check_func
        self.last_check_time = None
        self.last_status = None
    
    def check(self) -> bool:
        """Run health check."""
        try:
            self.last_status = self.check_func()
            self.last_check_time = time.time()
            return self.last_status
        except Exception as e:
            self.last_status = False
            self.last_check_time = time.time()
            return False


class HealthMonitor:
    """Monitor application health."""
    
    def __init__(self):
        """Initialize health monitor."""
        self.checks: Dict[str, HealthCheck] = {}
    
    def add_check(self, name: str, check_func: Callable[[], bool]) -> HealthCheck:
        """Add health check.
        
        Args:
            name: Check name
            check_func: Check function
            
        Returns:
            HealthCheck instance
        """
        check = HealthCheck(name, check_func)
        self.checks[name] = check
        return check
    
    def check_all(self) -> Dict[str, bool]:
        """Run all health checks.
        
        Returns:
            Dictionary of check results
        """
        results = {}
        for name, check in self.checks.items():
            results[name] = check.check()
        return results
    
    def is_healthy(self) -> bool:
        """Check if all checks pass."""
        return all(self.check_all().values())
    
    def get_status(self) -> Dict:
        """Get health status."""
        checks = self.check_all()
        
        return {
            "healthy": self.is_healthy(),
            "timestamp": time.time(),
            "checks": {
                name: {
                    "passed": status,
                    "last_check": self.checks[name].last_check_time
                }
                for name, status in checks.items()
            }
        }


class Profiler:
    """Simple performance profiler."""
    
    def __init__(self):
        """Initialize profiler."""
        self.timings: Dict[str, List[float]] = {}
    
    def time_function(self, func_name: str, duration: float):
        """Record function timing.
        
        Args:
            func_name: Function name
            duration: Execution time in seconds
        """
        if func_name not in self.timings:
            self.timings[func_name] = []
        
        self.timings[func_name].append(duration)
    
    def get_stats(self, func_name: str) -> Dict:
        """Get timing statistics.
        
        Args:
            func_name: Function name
            
        Returns:
            Timing statistics
        """
        if func_name not in self.timings:
            return {}
        
        times = self.timings[func_name]
        
        return {
            "count": len(times),
            "total": sum(times),
            "mean": sum(times) / len(times),
            "min": min(times),
            "max": max(times)
        }
    
    def get_all_stats(self) -> Dict:
        """Get all function statistics."""
        return {
            name: self.get_stats(name)
            for name in self.timings.keys()
        }
    
    def profile(self, func: Callable) -> Callable:
        """Decorator to profile function."""
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            
            self.time_function(func.__name__, duration)
            
            return result
        
        return wrapper


# Global metrics registry
_metrics = MetricsRegistry()


def get_metrics() -> MetricsRegistry:
    """Get global metrics registry."""
    return _metrics
