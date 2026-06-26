"""Rivet edge node — reverse proxy with caching, rate limiting, and bot detection.

Request pipeline:
  1. Bot detection  -> 403
  2. Rate limiting  -> 429
  3. Cache lookup   -> return on HIT
  4. Forward to origin (httpx)
  5. Cache the response (if cacheable)
  6. Emit metrics, return
"""
import time

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import Response, PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

import config
import metrics
from cache import LRUCache
from rate_limiter import RateLimiter
from bot_detection import BotDetector

app = FastAPI(title=f"Rivet Edge Node ({config.NODE_NAME})")

cache = LRUCache(max_size=config.CACHE_MAX_SIZE)
rate_limiter = RateLimiter(
    capacity=config.RATE_LIMIT_CAPACITY, per_seconds=config.RATE_LIMIT_WINDOW
)
bot_detector = BotDetector(
    path_threshold=config.BOT_PATH_THRESHOLD, window_seconds=config.BOT_WINDOW_SECONDS
)
client = httpx.AsyncClient(base_url=config.ORIGIN_URL, timeout=10.0)

metrics.node_up.labels(node=config.NODE_NAME).set(1)


def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def cacheable(method: str, path: str) -> bool:
    if method != "GET":
        return False
    if path.startswith("/api"):  # dynamic API responses are not cached
        return False
    return True


def ttl_from_headers(headers) -> int:
    cc = headers.get("cache-control", "")
    for part in cc.split(","):
        part = part.strip()
        if part.startswith("max-age="):
            try:
                return int(part.split("=", 1)[1])
            except ValueError:
                pass
        if part in ("no-store", "no-cache"):
            return 0
    return config.DEFAULT_TTL


# --- specific routes (must be declared before the catch-all) ---

@app.get("/health")
async def health():
    return {"status": "ok", "node": config.NODE_NAME}


@app.get("/metrics")
async def prometheus_metrics():
    stats = cache.stats()
    metrics.cache_hit_ratio.labels(node=config.NODE_NAME).set(stats["hit_ratio"])
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.delete("/cache")
async def purge_cache(path: str = ""):
    removed = cache.purge(path or None)
    return {"purged": removed, "path": path or "ALL"}


# --- catch-all proxy route ---

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, full_path: str):
    node = config.NODE_NAME
    start = time.perf_counter()
    path = "/" + full_path
    ip = client_ip(request)
    ua = request.headers.get("user-agent", "")

    # 1. Bot detection
    blocked, reason = bot_detector.is_blocked(ip, ua, path)
    if blocked:
        metrics.bot_blocked.labels(node=node, reason=reason).inc()
        metrics.requests_total.labels(node=node, status="403", path=path).inc()
        return PlainTextResponse(f"Forbidden: {reason}", status_code=403)

    # 2. Rate limiting — per-API-key if present, else per-IP
    api_key = request.headers.get("x-api-key")
    rl_key = f"key:{api_key}" if api_key else f"ip:{ip}"
    if not rate_limiter.allow(rl_key):
        metrics.rate_limited.labels(node=node).inc()
        metrics.requests_total.labels(node=node, status="429", path=path).inc()
        return PlainTextResponse("Too Many Requests", status_code=429)

    # 3. Cache lookup
    cache_key = f"{request.method}:{path}?{request.url.query}"
    is_cacheable = cacheable(request.method, path)
    if is_cacheable:
        cached = cache.get(cache_key)
        if cached is not None:
            body, status, headers = cached
            headers = dict(headers)
            headers["X-Cache"] = "HIT"
            headers["X-Edge-Node"] = node
            metrics.cache_hits.labels(node=node).inc()
            elapsed = (time.perf_counter() - start) * 1000
            metrics.latency_ms.labels(node=node, cache="hit").observe(elapsed)
            metrics.requests_total.labels(node=node, status=str(status), path=path).inc()
            return Response(content=body, status_code=status, headers=_safe(headers))
        metrics.cache_misses.labels(node=node).inc()

    # 4. Forward to origin
    try:
        body_in = await request.body()
        upstream = await client.request(
            request.method,
            path,
            params=dict(request.query_params),
            content=body_in,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
        )
    except httpx.HTTPError as e:
        metrics.requests_total.labels(node=node, status="502", path=path).inc()
        return PlainTextResponse(f"Bad Gateway: {e}", status_code=502)

    # 5. Cache store
    if is_cacheable and upstream.status_code == 200:
        ttl = ttl_from_headers(upstream.headers)
        if ttl > 0:
            cache.set(
                cache_key,
                (upstream.content, upstream.status_code, dict(upstream.headers)),
                ttl,
            )

    out_headers = _safe(dict(upstream.headers))
    out_headers["X-Cache"] = "MISS"
    out_headers["X-Edge-Node"] = node

    elapsed = (time.perf_counter() - start) * 1000
    metrics.latency_ms.labels(node=node, cache="miss").observe(elapsed)
    metrics.requests_total.labels(
        node=node, status=str(upstream.status_code), path=path
    ).inc()
    return Response(
        content=upstream.content, status_code=upstream.status_code, headers=out_headers
    )


def _safe(headers: dict) -> dict:
    """Drop hop-by-hop / length headers so Starlette can recompute them."""
    drop = {"content-length", "transfer-encoding", "content-encoding", "connection"}
    return {k: v for k, v in headers.items() if k.lower() not in drop}
