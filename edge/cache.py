"""Thread-safe in-memory LRU cache with per-key TTL.

Stores arbitrary values. The proxy stores (body, status, headers) tuples.
"""
import time
from collections import OrderedDict
from threading import Lock


class LRUCache:
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._store: "OrderedDict[str, tuple]" = OrderedDict()  # key -> (expiry_ts, value)
        self._lock = Lock()
        self.hits = 0
        self.misses = 0

    def get(self, key: str):
        with self._lock:
            item = self._store.get(key)
            if item is None:
                self.misses += 1
                return None
            expiry, value = item
            if expiry < time.time():
                del self._store[key]
                self.misses += 1
                return None
            self._store.move_to_end(key)  # mark as recently used
            self.hits += 1
            return value

    def set(self, key: str, value, ttl: int):
        with self._lock:
            self._store[key] = (time.time() + ttl, value)
            self._store.move_to_end(key)
            while len(self._store) > self.max_size:
                self._store.popitem(last=False)  # evict least-recently-used

    def purge(self, path: str | None = None) -> int:
        """Purge everything (path=None) or any key containing `path`."""
        with self._lock:
            if path is None:
                n = len(self._store)
                self._store.clear()
                return n
            doomed = [k for k in self._store if path in k]
            for k in doomed:
                del self._store[k]
            return len(doomed)

    def stats(self) -> dict:
        with self._lock:
            total = self.hits + self.misses
            ratio = (self.hits / total) if total else 0.0
            return {
                "size": len(self._store),
                "hits": self.hits,
                "misses": self.misses,
                "hit_ratio": round(ratio, 4),
            }
