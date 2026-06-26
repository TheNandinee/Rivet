"""Token-bucket rate limiter.

One bucket per key (per-IP or per-API-key). Capacity = burst size,
refilled at capacity/window tokens per second.
"""
import time
from threading import Lock


class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate          # tokens per second
        self.tokens = float(capacity)
        self.last = time.monotonic()

    def allow(self, cost: float = 1.0) -> bool:
        now = time.monotonic()
        elapsed = now - self.last
        self.last = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False


class RateLimiter:
    def __init__(self, capacity: int = 100, per_seconds: int = 10):
        self.capacity = capacity
        self.refill_rate = capacity / per_seconds
        self._buckets: dict[str, TokenBucket] = {}
        self._lock = Lock()

    def allow(self, key: str) -> bool:
        with self._lock:
            bucket = self._buckets.get(key)
            if bucket is None:
                bucket = TokenBucket(self.capacity, self.refill_rate)
                self._buckets[key] = bucket
            return bucket.allow()

    def update_limits(self, capacity: int, per_seconds: int):
        """Hook for the control plane to push new limits at runtime."""
        with self._lock:
            self.capacity = capacity
            self.refill_rate = capacity / per_seconds
            self._buckets.clear()  # reset so new limits apply cleanly
