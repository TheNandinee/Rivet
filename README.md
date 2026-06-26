# Rivet — Distributed Edge-Proxy Platform

A distributed edge caching, rate-limiting, and bot-protection proxy that simulates how a
CDN accelerates and protects traffic. Multiple dockerized edge nodes sit in front of an
origin server, cache responses, throttle abusive clients, and expose metrics to
Prometheus + Grafana.

## Quick start

```bash
docker compose up --build
```

This starts:

| Service     | URL                     | What it is                       |
|-------------|-------------------------|----------------------------------|
| edge-1      | http://localhost:8001   | Reverse proxy node               |
| edge-2      | http://localhost:8002   | Reverse proxy node               |
| edge-3      | http://localhost:8003   | Reverse proxy node               |
| origin      | http://localhost:9000   | Backend the edges proxy to       |
| prometheus  | http://localhost:9090   | Scrapes edge metrics every 15s   |
| grafana     | http://localhost:3000   | Dashboards (login admin/admin)   |

Try it:

```bash
curl -i http://localhost:8001/static/style.css   # cacheable -> first MISS, then HIT
curl -i http://localhost:8001/api/data           # slow, never cached
curl -i http://localhost:8001/metrics            # Prometheus metrics
```

Look at the `X-Cache` and `X-Edge-Node` response headers to see caching in action.

## Load tests

```bash
pip install httpx
python load_tests/scenarios.py cache       # cache hit ratio + latency drop
python load_tests/scenarios.py ratelimit   # burst -> 429s after the limit
python load_tests/scenarios.py bot         # blocked User-Agent -> 403
```

## Request pipeline (each edge node)

1. **Bot detection** — User-Agent blocklist + rapid path-enumeration -> `403`
2. **Rate limiting** — token bucket, per-API-key or per-IP -> `429`
3. **Cache lookup** — LRU + TTL, returns immediately on HIT
4. **Forward to origin** via httpx
5. **Cache the response** if cacheable (GET, non-`/api`, status 200)
6. **Emit metrics** and return

## Layout

```
rivet/
├── docker-compose.yml
├── edge/                 # proxy layer (networking) + security
│   ├── proxy.py          # FastAPI app, request pipeline
│   ├── cache.py          # LRU cache with TTL
│   ├── rate_limiter.py   # token bucket
│   ├── bot_detection.py  # abuse rules
│   ├── metrics.py        # Prometheus metrics
│   └── config.py         # env-driven config
├── origin/               # backend server
│   └── server.py
├── monitoring/
│   └── prometheus.yml
└── load_tests/
    └── scenarios.py
```

## Status / TODO

Done: reverse proxy, LRU cache + TTL, cache purge (`DELETE /cache?path=...`),
per-IP / per-API-key rate limiting, basic bot detection, Prometheus metrics,
3-node docker-compose with Prometheus + Grafana wired up.

Still to build (matches the original spec):
- **Observability** — Grafana dashboards (cache hit %, latency p95, 429/403 counts,
  node health). Prometheus is already scraping; dashboards just need building.
- **Control plane** — a separate service to push rate-limit / cache rules to edges at runtime.
- **Failover & routing** — health checks + latency-aware routing across nodes.
- **Distributed rate-limit state** — optional Redis so limits are shared across edges.

Tunable per edge via env vars (see `edge/config.py`): `DEFAULT_TTL`, `RATE_LIMIT_CAPACITY`,
`RATE_LIMIT_WINDOW`, `CACHE_MAX_SIZE`, `BOT_PATH_THRESHOLD`, `BOT_WINDOW_SECONDS`.
