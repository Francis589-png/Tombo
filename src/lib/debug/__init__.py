"""
Debug Library for TOMBO Language
Professional debugging, profiling, and memory analysis tools
"""

import time
import traceback
import sys
import os
import gc
import inspect
from datetime import datetime
from collections import defaultdict
from typing import Any, Callable, Optional, Dict, List, Tuple


class Breakpoint:
    """Manages breakpoints in code execution"""
    def __init__(self):
        self.breakpoints: Dict[str, List[int]] = defaultdict(list)
        self.enabled = True
    
    def set_breakpoint(self, filename: str, line: int) -> None:
        """Set a breakpoint at specific line"""
        self.breakpoints[filename].append(line)
    
    def clear_breakpoint(self, filename: str, line: int) -> None:
        """Clear a breakpoint"""
        if filename in self.breakpoints and line in self.breakpoints[filename]:
            self.breakpoints[filename].remove(line)
    
    def clear_all(self) -> None:
        """Clear all breakpoints"""
        self.breakpoints.clear()
    
    def is_breakpoint(self, filename: str, line: int) -> bool:
        """Check if breakpoint exists"""
        return self.enabled and line in self.breakpoints.get(filename, [])
    
    def list_breakpoints(self) -> Dict[str, List[int]]:
        """List all breakpoints"""
        return dict(self.breakpoints)


class Debugger:
    """Interactive debugger for stepping through code"""
    def __init__(self):
        self.breakpoints = Breakpoint()
        self.call_stack: List[Dict[str, Any]] = []
        self.variables: Dict[str, Any] = {}
        self.running = False
    
    def start_debugging(self, code: str) -> None:
        """Start debugging session"""
        self.running = True
        self.call_stack = []
        self.variables = {}
    
    def stop_debugging(self) -> None:
        """Stop debugging session"""
        self.running = False
    
    def step_over(self) -> None:
        """Execute next line"""
        pass
    
    def step_into(self) -> None:
        """Step into function call"""
        pass
    
    def step_out(self) -> None:
        """Step out of current function"""
        pass
    
    def continue_execution(self) -> None:
        """Continue until next breakpoint"""
        pass
    
    def watch_variable(self, name: str) -> Any:
        """Watch a variable"""
        return self.variables.get(name)
    
    def set_variable(self, name: str, value: Any) -> None:
        """Set variable value during debugging"""
        self.variables[name] = value
    
    def get_call_stack(self) -> List[Dict[str, Any]]:
        """Get current call stack"""
        return self.call_stack
    
    def get_locals(self) -> Dict[str, Any]:
        """Get local variables"""
        return self.variables.copy()


class Profiler:
    """CPU and performance profiling"""
    def __init__(self):
        self.call_times: Dict[str, List[float]] = defaultdict(list)
        self.call_counts: Dict[str, int] = defaultdict(int)
        self.start_time = 0.0
        self.is_running = False
    
    def start(self) -> None:
        """Start profiling"""
        self.is_running = True
        self.start_time = time.time()
    
    def stop(self) -> None:
        """Stop profiling"""
        self.is_running = False
    
    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile a function"""
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            self.call_times[func_name].append(elapsed)
            self.call_counts[func_name] += 1
            return result
        return wrapper
    
    def get_stats(self) -> Dict[str, Dict[str, float]]:
        """Get profiling statistics"""
        stats = {}
        for func_name, times in self.call_times.items():
            total_time = sum(times)
            stats[func_name] = {
                'calls': self.call_counts[func_name],
                'total_time': total_time,
                'avg_time': total_time / len(times) if times else 0,
                'min_time': min(times) if times else 0,
                'max_time': max(times) if times else 0
            }
        return stats
    
    def reset(self) -> None:
        """Reset profiler data"""
        self.call_times.clear()
        self.call_counts.clear()
    
    def print_stats(self) -> str:
        """Print formatted statistics"""
        stats = self.get_stats()
        output = "Function Call Statistics:\n"
        output += "=" * 60 + "\n"
        for func_name, data in sorted(stats.items()):
            output += f"{func_name}:\n"
            output += f"  Calls: {data['calls']}\n"
            output += f"  Total: {data['total_time']:.4f}s\n"
            output += f"  Avg:   {data['avg_time']:.4f}s\n"
            output += f"  Min:   {data['min_time']:.4f}s\n"
            output += f"  Max:   {data['max_time']:.4f}s\n"
        return output


class MemoryAnalyzer:
    """Analyze memory usage and leaks"""
    def __init__(self):
        self.snapshots: List[Dict[str, Any]] = []
        self.initial_size = 0
    
    def take_snapshot(self) -> Dict[str, Any]:
        """Take memory snapshot"""
        gc.collect()
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'objects': len(gc.get_objects()),
            'memory_info': self._get_memory_info()
        }
        self.snapshots.append(snapshot)
        return snapshot
    
    def _get_memory_info(self) -> Dict[str, int]:
        """Get current memory usage"""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            mem_info = process.memory_info()
            return {
                'rss': mem_info.rss,
                'vms': mem_info.vms
            }
        except ImportError:
            return {'rss': 0, 'vms': 0}
    
    def get_memory_growth(self) -> float:
        """Get memory growth since first snapshot"""
        if len(self.snapshots) < 2:
            return 0.0
        first = self.snapshots[0]['memory_info'].get('rss', 0)
        last = self.snapshots[-1]['memory_info'].get('rss', 0)
        return last - first
    
    def get_object_growth(self) -> int:
        """Get object count growth"""
        if len(self.snapshots) < 2:
            return 0
        return self.snapshots[-1]['objects'] - self.snapshots[0]['objects']
    
    def detect_leaks(self) -> List[str]:
        """Detect potential memory leaks"""
        if len(self.snapshots) < 2:
            return []
        
        leaks = []
        growth = self.get_object_growth()
        if growth > 1000:
            leaks.append(f"Large object growth: +{growth} objects")
        
        mem_growth = self.get_memory_growth()
        if mem_growth > 100_000_000:  # 100MB
            leaks.append(f"Large memory growth: +{mem_growth / 1_000_000:.1f}MB")
        
        return leaks
    
    def print_report(self) -> str:
        """Print memory analysis report"""
        output = "Memory Analysis Report\n"
        output += "=" * 60 + "\n"
        
        for i, snapshot in enumerate(self.snapshots):
            output += f"Snapshot {i+1} ({snapshot['timestamp']}):\n"
            output += f"  Objects: {snapshot['objects']}\n"
            output += f"  RSS: {snapshot['memory_info'].get('rss', 0) / 1_000_000:.1f}MB\n"
        
        output += "\nGrowth Analysis:\n"
        output += f"  Object Growth: {self.get_object_growth()}\n"
        output += f"  Memory Growth: {self.get_memory_growth() / 1_000_000:.1f}MB\n"
        
        leaks = self.detect_leaks()
        if leaks:
            output += "\nPotential Leaks:\n"
            for leak in leaks:
                output += f"  - {leak}\n"
        
        return output


class Logger:
    """Debug logging with levels"""
    def __init__(self, name: str = "TOMBO"):
        self.name = name
        self.logs: List[Tuple[str, str, str]] = []
        self.level = "INFO"
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self._log("DEBUG", message)
    
    def info(self, message: str) -> None:
        """Log info message"""
        self._log("INFO", message)
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self._log("WARNING", message)
    
    def error(self, message: str) -> None:
        """Log error message"""
        self._log("ERROR", message)
    
    def _log(self, level: str, message: str) -> None:
        """Internal log method"""
        timestamp = datetime.now().isoformat()
        self.logs.append((timestamp, level, message))
        print(f"[{level}] {self.name}: {message}")
    
    def get_logs(self) -> List[Tuple[str, str, str]]:
        """Get all logs"""
        return self.logs.copy()
    
    def clear_logs(self) -> None:
        """Clear log history"""
        self.logs.clear()


class TraceRecorder:
    """Record function calls and returns"""
    def __init__(self):
        self.traces: List[Dict[str, Any]] = []
        self.recording = False
    
    def start_recording(self) -> None:
        """Start recording traces"""
        self.recording = True
        sys.settrace(self._trace_function)
    
    def stop_recording(self) -> None:
        """Stop recording traces"""
        self.recording = False
        sys.settrace(None)
    
    def _trace_function(self, frame, event, arg):
        """Internal trace function"""
        if not self.recording:
            return None
        
        if event == 'call':
            self.traces.append({
                'type': 'call',
                'function': frame.f_code.co_name,
                'filename': frame.f_code.co_filename,
                'line': frame.f_lineno,
                'timestamp': time.time()
            })
        elif event == 'return':
            self.traces.append({
                'type': 'return',
                'function': frame.f_code.co_name,
                'value': str(arg)[:100],
                'timestamp': time.time()
            })
        
        return self._trace_function
    
    def get_traces(self) -> List[Dict[str, Any]]:
        """Get recorded traces"""
        return self.traces.copy()
    
    def clear_traces(self) -> None:
        """Clear trace history"""
        self.traces.clear()


class AssertionHelper:
    """Helper for assertions and validations"""
    @staticmethod
    def assert_true(condition: bool, message: str = "Assertion failed") -> None:
        """Assert condition is true"""
        if not condition:
            raise AssertionError(message)
    
    @staticmethod
    def assert_false(condition: bool, message: str = "Assertion failed") -> None:
        """Assert condition is false"""
        if condition:
            raise AssertionError(message)
    
    @staticmethod
    def assert_equal(a: Any, b: Any, message: str = "") -> None:
        """Assert values are equal"""
        if a != b:
            raise AssertionError(f"{message}: {a} != {b}")
    
    @staticmethod
    def assert_not_equal(a: Any, b: Any, message: str = "") -> None:
        """Assert values are not equal"""
        if a == b:
            raise AssertionError(f"{message}: {a} == {b}")
    
    @staticmethod
    def assert_in(value: Any, container: Any, message: str = "") -> None:
        """Assert value is in container"""
        if value not in container:
            raise AssertionError(f"{message}: {value} not in {container}")
    
    @staticmethod
    def assert_raises(exception_type: type, func: Callable, *args, **kwargs) -> None:
        """Assert function raises exception"""
        try:
            func(*args, **kwargs)
            raise AssertionError(f"Expected {exception_type.__name__} but no exception was raised")
        except exception_type:
            pass


# Module-level instances
debugger = Debugger()
profiler = Profiler()
memory_analyzer = MemoryAnalyzer()
logger = Logger("TOMBO")
trace_recorder = TraceRecorder()
assertion = AssertionHelper()


# Public API
__all__ = [
    'Breakpoint',
    'Debugger',
    'Profiler',
    'MemoryAnalyzer',
    'Logger',
    'TraceRecorder',
    'AssertionHelper',
    'debugger',
    'profiler',
    'memory_analyzer',
    'logger',
    'trace_recorder',
    'assertion'
]
