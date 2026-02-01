"""
TOMBO Cache Library - In-memory caching with TTL and strategies
Provides caching with expiration, eviction policies, and cache statistics.
"""

import time
from typing import Dict, Any, Optional, Callable, List


class CacheEntry:
    """Cache entry with TTL and metadata."""
    
    def __init__(self, key: str, value: Any, ttl: Optional[int] = None):
        """Initialize cache entry.
        
        Args:
            key: Entry key
            value: Cached value
            ttl: Time to live in seconds (None = never expires)
        """
        self.key = key
        self.value = value
        self.ttl = ttl
        self.created_at = time.time()
        self.accessed_at = self.created_at
        self.hit_count = 0
    
    def is_expired(self) -> bool:
        """Check if entry is expired."""
        if self.ttl is None:
            return False
        
        age = time.time() - self.created_at
        return age > self.ttl
    
    def get(self) -> Any:
        """Get value and update access time."""
        self.accessed_at = time.time()
        self.hit_count += 1
        return self.value
    
    def to_dict(self) -> Dict:
        """Convert entry to dictionary."""
        return {
            "key": self.key,
            "value": self.value,
            "ttl": self.ttl,
            "created_at": self.created_at,
            "accessed_at": self.accessed_at,
            "hit_count": self.hit_count,
            "expired": self.is_expired()
        }


class Cache:
    """In-memory cache with TTL support."""
    
    def __init__(self, max_size: int = 1000, eviction_policy: str = "LRU"):
        """Initialize cache.
        
        Args:
            max_size: Maximum number of entries
            eviction_policy: Eviction policy (LRU, LFU, FIFO)
        """
        self.max_size = max_size
        self.eviction_policy = eviction_policy
        self._cache: Dict[str, CacheEntry] = {}
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "expirations": 0
        }
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set cache value.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
        """
        # Clean up expired entries
        self._cleanup_expired()
        
        # Evict if needed
        if len(self._cache) >= self.max_size and key not in self._cache:
            self._evict_one()
        
        self._cache[key] = CacheEntry(key, value, ttl)
    
    def get(self, key: str) -> Any:
        """Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if key not in self._cache:
            self._stats["misses"] += 1
            return None
        
        entry = self._cache[key]
        
        if entry.is_expired():
            del self._cache[key]
            self._stats["expirations"] += 1
            self._stats["misses"] += 1
            return None
        
        self._stats["hits"] += 1
        return entry.get()
    
    def has(self, key: str) -> bool:
        """Check if key exists and is not expired."""
        if key not in self._cache:
            return False
        
        if self._cache[key].is_expired():
            del self._cache[key]
            return False
        
        return True
    
    def delete(self, key: str) -> bool:
        """Delete cache entry.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False if not found
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self):
        """Clear all cache entries."""
        self._cache.clear()
    
    def size(self) -> int:
        """Get number of entries."""
        return len(self._cache)
    
    def _cleanup_expired(self):
        """Remove expired entries."""
        expired_keys = [key for key, entry in self._cache.items() if entry.is_expired()]
        for key in expired_keys:
            del self._cache[key]
            self._stats["expirations"] += 1
    
    def _evict_one(self):
        """Evict one entry based on policy."""
        if not self._cache:
            return
        
        if self.eviction_policy == "LRU":
            # Least Recently Used
            key = min(self._cache.keys(), 
                     key=lambda k: self._cache[k].accessed_at)
        elif self.eviction_policy == "LFU":
            # Least Frequently Used
            key = min(self._cache.keys(),
                     key=lambda k: self._cache[k].hit_count)
        elif self.eviction_policy == "FIFO":
            # First In, First Out
            key = min(self._cache.keys(),
                     key=lambda k: self._cache[k].created_at)
        else:
            # Default to LRU
            key = min(self._cache.keys(),
                     key=lambda k: self._cache[k].accessed_at)
        
        del self._cache[key]
        self._stats["evictions"] += 1
    
    def stats(self) -> Dict:
        """Get cache statistics."""
        total_requests = self._stats["hits"] + self._stats["misses"]
        hit_rate = (self._stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate": hit_rate,
            "evictions": self._stats["evictions"],
            "expirations": self._stats["expirations"]
        }
    
    def entries(self) -> List[Dict]:
        """Get all cache entries."""
        return [entry.to_dict() for entry in self._cache.values()]


class CacheDecorator:
    """Decorator for caching function results."""
    
    def __init__(self, cache: Cache, ttl: Optional[int] = None):
        """Initialize decorator.
        
        Args:
            cache: Cache instance
            ttl: Time to live for cached results
        """
        self.cache = cache
        self.ttl = ttl
    
    def __call__(self, func: Callable) -> Callable:
        """Wrap function with caching."""
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            
            # Try to get from cache
            result = self.cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            self.cache.set(cache_key, result, self.ttl)
            
            return result
        
        return wrapper


class CacheManager:
    """Manage multiple caches."""
    
    def __init__(self):
        """Initialize cache manager."""
        self._caches: Dict[str, Cache] = {}
    
    def create_cache(self, name: str, max_size: int = 1000, 
                    eviction_policy: str = "LRU") -> Cache:
        """Create named cache.
        
        Args:
            name: Cache name
            max_size: Maximum entries
            eviction_policy: Eviction policy
            
        Returns:
            Cache instance
        """
        cache = Cache(max_size, eviction_policy)
        self._caches[name] = cache
        return cache
    
    def get_cache(self, name: str) -> Optional[Cache]:
        """Get cache by name.
        
        Args:
            name: Cache name
            
        Returns:
            Cache instance or None
        """
        return self._caches.get(name)
    
    def delete_cache(self, name: str) -> bool:
        """Delete cache.
        
        Args:
            name: Cache name
            
        Returns:
            True if deleted
        """
        if name in self._caches:
            del self._caches[name]
            return True
        return False
    
    def list_caches(self) -> List[str]:
        """List all cache names."""
        return list(self._caches.keys())
    
    def all_stats(self) -> Dict:
        """Get stats for all caches."""
        return {
            name: cache.stats()
            for name, cache in self._caches.items()
        }


# Global cache manager
_manager = CacheManager()


def create_cache(name: str = "default", max_size: int = 1000, 
                 eviction_policy: str = "LRU") -> Cache:
    """Create or get cache."""
    if _manager.get_cache(name):
        return _manager.get_cache(name)
    return _manager.create_cache(name, max_size, eviction_policy)


def get_cache(name: str = "default") -> Optional[Cache]:
    """Get cache by name."""
    return _manager.get_cache(name)


def cache_result(ttl: Optional[int] = None, cache_name: str = "default"):
    """Decorator to cache function results."""
    def decorator(func):
        cache = create_cache(cache_name)
        return CacheDecorator(cache, ttl)(func)
    return decorator
