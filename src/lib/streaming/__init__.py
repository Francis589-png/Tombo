"""
TOMBO Streaming Library - Real-time data streaming and processing
Data streams, windows, aggregations, and backpressure handling.
"""

import time
from typing import Dict, List, Callable, Any, Optional, Deque
from collections import deque


class StreamEvent:
    """Stream event with timestamp."""
    
    def __init__(self, data: Any, timestamp: float = None):
        """Initialize event.
        
        Args:
            data: Event data
            timestamp: Event timestamp (auto-set if not provided)
        """
        self.data = data
        self.timestamp = timestamp or time.time()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "data": self.data,
            "timestamp": self.timestamp
        }


class Stream:
    """Base data stream."""
    
    def __init__(self, name: str = "stream"):
        """Initialize stream.
        
        Args:
            name: Stream name
        """
        self.name = name
        self.listeners: List[Callable] = []
        self.is_active = False
    
    def emit(self, data: Any):
        """Emit event to stream."""
        event = StreamEvent(data)
        for listener in self.listeners:
            listener(event)
    
    def on_event(self, handler: Callable):
        """Register event handler."""
        self.listeners.append(handler)
        return self
    
    def start(self):
        """Start stream."""
        self.is_active = True
    
    def stop(self):
        """Stop stream."""
        self.is_active = False


class FilterStream(Stream):
    """Stream with filtering."""
    
    def __init__(self, source: Stream, predicate: Callable[[Any], bool]):
        """Initialize filter stream.
        
        Args:
            source: Source stream
            predicate: Filter predicate
        """
        super().__init__("filter_stream")
        self.source = source
        self.predicate = predicate
        
        self.source.on_event(self._handle_event)
    
    def _handle_event(self, event: StreamEvent):
        """Handle source event."""
        if self.predicate(event.data):
            self.emit(event.data)


class MapStream(Stream):
    """Stream with transformation."""
    
    def __init__(self, source: Stream, transform: Callable[[Any], Any]):
        """Initialize map stream.
        
        Args:
            source: Source stream
            transform: Transformation function
        """
        super().__init__("map_stream")
        self.source = source
        self.transform = transform
        
        self.source.on_event(self._handle_event)
    
    def _handle_event(self, event: StreamEvent):
        """Handle source event."""
        try:
            transformed = self.transform(event.data)
            self.emit(transformed)
        except Exception as e:
            print(f"Transform error: {e}")


class TumblingWindowStream(Stream):
    """Stream with tumbling window aggregation."""
    
    def __init__(self, source: Stream, window_size: int, 
                 aggregator: Callable[[List], Any]):
        """Initialize tumbling window stream.
        
        Args:
            source: Source stream
            window_size: Window size in events
            aggregator: Aggregation function
        """
        super().__init__("tumbling_window_stream")
        self.source = source
        self.window_size = window_size
        self.aggregator = aggregator
        self.buffer: List = []
        
        self.source.on_event(self._handle_event)
    
    def _handle_event(self, event: StreamEvent):
        """Handle source event."""
        self.buffer.append(event.data)
        
        if len(self.buffer) >= self.window_size:
            result = self.aggregator(self.buffer)
            self.emit(result)
            self.buffer = []


class SlidingWindowStream(Stream):
    """Stream with sliding window aggregation."""
    
    def __init__(self, source: Stream, window_size: int, slide_size: int,
                 aggregator: Callable[[List], Any]):
        """Initialize sliding window stream.
        
        Args:
            source: Source stream
            window_size: Window size in events
            slide_size: Slide size in events
            aggregator: Aggregation function
        """
        super().__init__("sliding_window_stream")
        self.source = source
        self.window_size = window_size
        self.slide_size = slide_size
        self.aggregator = aggregator
        self.buffer: Deque = deque(maxlen=window_size)
        self.event_count = 0
        
        self.source.on_event(self._handle_event)
    
    def _handle_event(self, event: StreamEvent):
        """Handle source event."""
        self.buffer.append(event.data)
        self.event_count += 1
        
        if self.event_count % self.slide_size == 0:
            if len(self.buffer) == self.window_size:
                result = self.aggregator(list(self.buffer))
                self.emit(result)


class TimeWindowStream(Stream):
    """Stream with time-based window aggregation."""
    
    def __init__(self, source: Stream, window_duration: float,
                 aggregator: Callable[[List], Any]):
        """Initialize time window stream.
        
        Args:
            source: Source stream
            window_duration: Window duration in seconds
            aggregator: Aggregation function
        """
        super().__init__("time_window_stream")
        self.source = source
        self.window_duration = window_duration
        self.aggregator = aggregator
        self.buffer: List[Any] = []
        self.window_start = time.time()
        
        self.source.on_event(self._handle_event)
    
    def _handle_event(self, event: StreamEvent):
        """Handle source event."""
        now = time.time()
        
        if now - self.window_start >= self.window_duration:
            # Emit aggregation
            if self.buffer:
                result = self.aggregator(self.buffer)
                self.emit(result)
            
            # Start new window
            self.buffer = []
            self.window_start = now
        
        self.buffer.append(event.data)


class StreamProcessor:
    """Process streams with backpressure."""
    
    def __init__(self, max_buffer: int = 1000):
        """Initialize processor.
        
        Args:
            max_buffer: Maximum buffer size
        """
        self.streams: Dict[str, Stream] = {}
        self.buffer: Deque = deque(maxlen=max_buffer)
        self.processed = 0
        self.dropped = 0
    
    def add_stream(self, name: str, stream: Stream):
        """Add stream to processor."""
        self.streams[name] = stream
        stream.on_event(self._handle_event)
    
    def _handle_event(self, event: StreamEvent):
        """Handle event from stream."""
        try:
            self.buffer.append(event)
            self.processed += 1
        except:
            # Backpressure: buffer full
            self.dropped += 1
    
    def get_stats(self) -> Dict:
        """Get processor statistics."""
        return {
            "streams": len(self.streams),
            "buffered_events": len(self.buffer),
            "processed": self.processed,
            "dropped": self.dropped
        }


class RateLimiter:
    """Rate limit stream events."""
    
    def __init__(self, source: Stream, events_per_second: float):
        """Initialize rate limiter.
        
        Args:
            source: Source stream
            events_per_second: Maximum events per second
        """
        self.source = source
        self.rate = events_per_second
        self.min_interval = 1.0 / events_per_second if events_per_second > 0 else 0
        self.last_event_time = 0
        
        self.source.on_event(self._handle_event)
    
    def _handle_event(self, event: StreamEvent):
        """Handle event with rate limiting."""
        now = time.time()
        time_since_last = now - self.last_event_time
        
        if time_since_last >= self.min_interval:
            self.last_event_time = now
            return event
        
        # Backpressure: wait
        wait_time = self.min_interval - time_since_last
        time.sleep(wait_time)
        self.last_event_time = time.time()
        return event


class StreamBuffer:
    """Buffer for stream batching."""
    
    def __init__(self, source: Stream, batch_size: int, 
                 timeout: float = None):
        """Initialize buffer.
        
        Args:
            source: Source stream
            batch_size: Batch size
            timeout: Optional timeout in seconds
        """
        self.source = source
        self.batch_size = batch_size
        self.timeout = timeout
        self.buffer: List = []
        self.batch_start = time.time()
        self.listeners: List[Callable] = []
        
        self.source.on_event(self._handle_event)
    
    def _handle_event(self, event: StreamEvent):
        """Handle event."""
        now = time.time()
        
        # Check timeout
        if self.timeout and (now - self.batch_start) >= self.timeout:
            if self.buffer:
                self._emit_batch()
            self.buffer = []
            self.batch_start = now
        
        self.buffer.append(event.data)
        
        if len(self.buffer) >= self.batch_size:
            self._emit_batch()
            self.buffer = []
            self.batch_start = now
    
    def _emit_batch(self):
        """Emit batch to listeners."""
        for listener in self.listeners:
            listener(self.buffer.copy())
    
    def on_batch(self, handler: Callable):
        """Register batch handler."""
        self.listeners.append(handler)


class StreamMerger:
    """Merge multiple streams."""
    
    def __init__(self, *streams: Stream):
        """Initialize merger.
        
        Args:
            streams: Streams to merge
        """
        self.output = Stream("merged")
        
        for stream in streams:
            stream.on_event(self._handle_event)
    
    def _handle_event(self, event: StreamEvent):
        """Handle event from any stream."""
        self.output.emit(event.data)
    
    def get_stream(self) -> Stream:
        """Get merged output stream."""
        return self.output
