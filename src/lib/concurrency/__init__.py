"""
TOMBO Concurrency Library
Threads, Async/Await, Parallelism
"""

import time
from typing import Callable, List, Optional, Any
from threading import Thread, Lock, RLock, Semaphore, Event, Condition
from queue import Queue


# ============================================================================
# THREADING
# ============================================================================

class ThreadWorker(Thread):
    """Thread worker wrapper"""
    
    def __init__(self, target: Callable, args=None, kwargs=None, daemon: bool = False):
        super().__init__()
        self.target = target
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.daemon = daemon
        self.result = None
        self.exception = None
    
    def run(self):
        """Execute thread target"""
        try:
            self.result = self.target(*self.args, **self.kwargs)
        except Exception as e:
            self.exception = e
    
    def get_result(self):
        """Get thread result"""
        self.join()
        if self.exception:
            raise self.exception
        return self.result


class ThreadPool:
    """Thread pool for parallel task execution"""
    
    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self.tasks = Queue()
        self.workers = []
        self.running = False
    
    def start(self):
        """Start thread pool"""
        self.running = True
        for _ in range(self.num_workers):
            worker = Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def _worker_loop(self):
        """Worker thread loop"""
        while self.running:
            try:
                task = self.tasks.get(timeout=0.1)
                if task is None:
                    break
                func, args, kwargs = task
                func(*args, **kwargs)
                self.tasks.task_done()
            except:
                pass
    
    def submit(self, func: Callable, *args, **kwargs):
        """Submit task to pool"""
        self.tasks.put((func, args, kwargs))
    
    def wait_all(self):
        """Wait for all tasks to complete"""
        self.tasks.join()
    
    def shutdown(self):
        """Shutdown thread pool"""
        self.running = False
        for _ in range(self.num_workers):
            self.tasks.put(None)
        for worker in self.workers:
            worker.join()


class ReentrantLock:
    """Reentrant mutual exclusion lock"""
    
    def __init__(self):
        self.lock = RLock()
    
    def acquire(self, blocking: bool = True, timeout: float = -1):
        """Acquire lock"""
        return self.lock.acquire(blocking, timeout)
    
    def release(self):
        """Release lock"""
        self.lock.release()
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class SimpleLock:
    """Simple mutual exclusion lock"""
    
    def __init__(self):
        self.lock = Lock()
    
    def acquire(self, blocking: bool = True, timeout: float = -1):
        """Acquire lock"""
        return self.lock.acquire(blocking, timeout)
    
    def release(self):
        """Release lock"""
        self.lock.release()
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class Semaphore:
    """Semaphore for resource counting"""
    
    def __init__(self, count: int = 1):
        self.semaphore = Semaphore(count)
    
    def acquire(self, blocking: bool = True, timeout: float = -1):
        """Acquire semaphore"""
        return self.semaphore.acquire(blocking, timeout)
    
    def release(self):
        """Release semaphore"""
        self.semaphore.release()


class Event:
    """Event for signaling between threads"""
    
    def __init__(self):
        self.event = Event()
    
    def set(self):
        """Set event flag"""
        self.event.set()
    
    def clear(self):
        """Clear event flag"""
        self.event.clear()
    
    def is_set(self) -> bool:
        """Check if event is set"""
        return self.event.is_set()
    
    def wait(self, timeout: Optional[float] = None) -> bool:
        """Wait for event"""
        return self.event.wait(timeout)


class Condition:
    """Condition variable for thread synchronization"""
    
    def __init__(self):
        self.condition = Condition()
    
    def acquire(self):
        """Acquire condition"""
        self.condition.acquire()
    
    def release(self):
        """Release condition"""
        self.condition.release()
    
    def wait(self, timeout: Optional[float] = None):
        """Wait for condition"""
        return self.condition.wait(timeout)
    
    def notify(self, n: int = 1):
        """Notify waiting threads"""
        self.condition.notify(n)
    
    def notify_all(self):
        """Notify all waiting threads"""
        self.condition.notify_all()


# ============================================================================
# ASYNC/AWAIT SIMULATION
# ============================================================================

class Future:
    """Represents a result that will be available in the future"""
    
    def __init__(self):
        self.result = None
        self.exception = None
        self.done = False
        self.callbacks = []
        self.lock = Lock()
        self.event = Event()
    
    def set_result(self, result: Any):
        """Set the result"""
        with self.lock:
            if self.done:
                raise RuntimeError("Future result already set")
            self.result = result
            self.done = True
            self.event.set()
            for callback in self.callbacks:
                callback(self)
    
    def set_exception(self, exception: Exception):
        """Set an exception"""
        with self.lock:
            if self.done:
                raise RuntimeError("Future result already set")
            self.exception = exception
            self.done = True
            self.event.set()
            for callback in self.callbacks:
                callback(self)
    
    def result(self, timeout: Optional[float] = None) -> Any:
        """Get the result"""
        if not self.done:
            self.event.wait(timeout)
        if self.exception:
            raise self.exception
        return self.result
    
    def is_done(self) -> bool:
        """Check if result is ready"""
        return self.done
    
    def add_callback(self, callback: Callable):
        """Add callback for when result is ready"""
        with self.lock:
            if self.done:
                callback(self)
            else:
                self.callbacks.append(callback)


class Task:
    """Async task wrapper"""
    
    def __init__(self, coro: Callable):
        self.coro = coro
        self.future = Future()
        self.state = 'pending'  # pending, running, done
    
    def run(self):
        """Execute the coroutine"""
        try:
            self.state = 'running'
            result = self.coro()
            self.state = 'done'
            self.future.set_result(result)
        except Exception as e:
            self.state = 'done'
            self.future.set_exception(e)
    
    def result(self, timeout: Optional[float] = None):
        """Get task result"""
        return self.future.result(timeout)
    
    def is_done(self) -> bool:
        """Check if task is done"""
        return self.state == 'done'


class EventLoop:
    """Simple event loop for async execution"""
    
    def __init__(self):
        self.tasks = []
        self.running = False
    
    def create_task(self, coro: Callable) -> Task:
        """Create and schedule a task"""
        task = Task(coro)
        self.tasks.append(task)
        return task
    
    def run_until_complete(self, coro: Callable):
        """Run coroutine until it completes"""
        task = self.create_task(coro)
        self.run()
        return task.result()
    
    def run(self):
        """Run event loop"""
        self.running = True
        while self.tasks and self.running:
            task = self.tasks.pop(0)
            if not task.is_done():
                task.run()
            if not task.is_done():
                self.tasks.append(task)
        self.running = False
    
    def stop(self):
        """Stop event loop"""
        self.running = False


# ============================================================================
# PROCESS OPERATIONS (Simulated)
# ============================================================================

class Process:
    """Process wrapper"""
    
    def __init__(self, target: Callable, args=None, kwargs=None):
        self.target = target
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.pid = None
        self.running = False
        self.result = None
    
    def start(self):
        """Start process"""
        self.running = True
        # In real implementation, would fork process
        self.pid = id(self)
        return True
    
    def join(self, timeout: Optional[float] = None):
        """Wait for process to finish"""
        self.running = False
        return True
    
    def terminate(self):
        """Terminate process"""
        self.running = False


class ProcessPool:
    """Pool of worker processes"""
    
    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self.processes = []
    
    def map(self, func: Callable, items: List[Any]) -> List[Any]:
        """Map function across items in parallel"""
        results = []
        for item in items:
            results.append(func(item))
        return results
    
    def close(self):
        """Close process pool"""
        for proc in self.processes:
            if proc.running:
                proc.terminate()


# ============================================================================
# PARALLEL EXECUTION
# ============================================================================

class ParallelExecutor:
    """Execute functions in parallel"""
    
    @staticmethod
    def map_parallel(func: Callable, items: List[Any], num_workers: int = 4) -> List[Any]:
        """Execute function in parallel on items"""
        pool = ThreadPool(num_workers)
        pool.start()
        
        results = [None] * len(items)
        
        def worker_func(idx, item):
            results[idx] = func(item)
        
        for idx, item in enumerate(items):
            pool.submit(worker_func, idx, item)
        
        pool.wait_all()
        pool.shutdown()
        return results
    
    @staticmethod
    def parallel_for(func: Callable, start: int, end: int, num_workers: int = 4):
        """Execute function in parallel for range"""
        pool = ThreadPool(num_workers)
        pool.start()
        
        for i in range(start, end):
            pool.submit(func, i)
        
        pool.wait_all()
        pool.shutdown()


# ============================================================================
# PUBLIC API FUNCTIONS
# ============================================================================

def create_thread(target: Callable, args=None, daemon: bool = False) -> ThreadWorker:
    """Create thread"""
    return ThreadWorker(target, args, daemon=daemon)

def create_lock() -> SimpleLock:
    """Create simple lock"""
    return SimpleLock()

def create_rlock() -> ReentrantLock:
    """Create reentrant lock"""
    return ReentrantLock()

def create_semaphore(count: int = 1) -> Semaphore:
    """Create semaphore"""
    return Semaphore(count)

def create_event() -> Event:
    """Create event"""
    return Event()

def create_condition() -> Condition:
    """Create condition variable"""
    return Condition()

def create_thread_pool(num_workers: int = 4) -> ThreadPool:
    """Create thread pool"""
    pool = ThreadPool(num_workers)
    pool.start()
    return pool

def create_process_pool(num_workers: int = 4) -> ProcessPool:
    """Create process pool"""
    return ProcessPool(num_workers)

def create_future() -> Future:
    """Create future"""
    return Future()

def create_task(coro: Callable) -> Task:
    """Create async task"""
    return Task(coro)

def create_event_loop() -> EventLoop:
    """Create event loop"""
    return EventLoop()

def run_in_parallel(func: Callable, items: List[Any], num_workers: int = 4) -> List[Any]:
    """Run function in parallel"""
    return ParallelExecutor.map_parallel(func, items, num_workers)

def parallel_for(func: Callable, start: int, end: int, num_workers: int = 4):
    """Run loop in parallel"""
    ParallelExecutor.parallel_for(func, start, end, num_workers)

def sleep_async(duration: float):
    """Async sleep"""
    time.sleep(duration)
