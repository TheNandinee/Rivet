"""Quick load tests you can run from your Mac (no Docker needed for the runner).

    pip install httpx
    python load_tests/scenarios.py cache
    python load_tests/scenarios.py ratelimit
    python load_tests/scenarios.py bot

These hit the edge on http://localhost:8001 (edge-1). Spin the stack up first
with `docker compose up --build`.
"""
import sys
import time
import statistics
import httpx

EDGE = "http://localhost:8001"


def cache_test(n: int = 500):
    """Same endpoint hit many times -> hit ratio should climb, latency drop."""
    url = f"{EDGE}/static/style.css"
    first_latencies, hit_latencies = [], []
    with httpx.Client(timeout=10) as c:
        for i in range(n):
            t = time.perf_counter()
            r = c.get(url)
            ms = (time.perf_counter() - t) * 1000
            (hit_latencies if r.headers.get("X-Cache") == "HIT" else first_latencies).append(ms)
    print(f"requests: {n}")
    print(f"MISS count: {len(first_latencies)}  HIT count: {len(hit_latencies)}")
    if first_latencies:
        print(f"MISS p50: {statistics.median(first_latencies):.1f} ms")
    if hit_latencies:
        print(f"HIT  p50: {statistics.median(hit_latencies):.1f} ms")
    print(f"hit ratio: {len(hit_latencies)/n*100:.1f}%")


def ratelimit_test(n: int = 300):
    """Burst from one client -> first ~100 succeed, rest get 429."""
    url = f"{EDGE}/api/data"
    codes = {}
    with httpx.Client(timeout=10) as c:
        for _ in range(n):
            r = c.get(url)
            codes[r.status_code] = codes.get(r.status_code, 0) + 1
    print(f"sent {n} rapid requests -> status counts: {codes}")
    print("expect ~100x 200 then 429s (default limit = 100 req / 10s per IP)")


def bot_test():
    """Send a blocked User-Agent -> expect 403."""
    with httpx.Client(timeout=10) as c:
        r = c.get(f"{EDGE}/static/x.css", headers={"User-Agent": "sqlmap/1.0"})
        print(f"sqlmap UA -> {r.status_code} ({r.text[:60]})")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "cache"
    {"cache": cache_test, "ratelimit": ratelimit_test, "bot": bot_test}.get(
        mode, cache_test
    )()
