"""Lightweight abuse / bot detection.

Two rules to start (extend these for Week 6 of the spec):
  1. User-Agent blocklist (scanners, known bad tools).
  2. Rapid path enumeration: same IP hitting many distinct paths fast.
"""
import time
from threading import Lock

BLOCKED_UA = ["sqlmap", "nikto", "masscan", "nmap", "dirbuster", "evil-scanner", "badbot"]


class BotDetector:
    def __init__(self, path_threshold: int = 10, window_seconds: int = 5):
        self.path_threshold = path_threshold
        self.window_seconds = window_seconds
        self._activity: dict[str, list[tuple[float, str]]] = {}
        self._lock = Lock()

    def is_blocked(self, ip: str, user_agent: str, path: str):
        ua = (user_agent or "").lower()
        for bad in BLOCKED_UA:
            if bad in ua:
                return True, f"blocked_user_agent:{bad}"

        now = time.time()
        with self._lock:
            events = self._activity.setdefault(ip, [])
            events.append((now, path))
            cutoff = now - self.window_seconds
            events[:] = [(t, p) for (t, p) in events if t >= cutoff]
            distinct_paths = {p for (_, p) in events}
            if len(distinct_paths) >= self.path_threshold:
                return True, "rapid_path_enumeration"

        return False, ""
