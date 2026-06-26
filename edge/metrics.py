"""Prometheus metric definitions shared across the edge node."""
from prometheus_client import Counter, Histogram, Gauge

requests_total = Counter(
    "edge_requests_total", "Total requests handled", ["node", "status", "path"]
)
latency_ms = Histogram(
    "edge_latency_ms", "Request latency in milliseconds", ["node", "cache"],
    buckets=(1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500),
)
cache_hits = Counter("edge_cache_hits_total", "Cache hits", ["node"])
cache_misses = Counter("edge_cache_misses_total", "Cache misses", ["node"])
cache_hit_ratio = Gauge("edge_cache_hit_ratio", "Cache hit ratio (0-1)", ["node"])
rate_limited = Counter("edge_rate_limited_total", "Requests rejected with 429", ["node"])
bot_blocked = Counter("edge_bot_blocked_total", "Requests blocked as bots", ["node", "reason"])
node_up = Gauge("edge_node_up", "1 if the node is up", ["node"])
