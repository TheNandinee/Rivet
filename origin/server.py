"""Rivet origin server.

A simple backend the edge nodes proxy to. Static routes are cacheable;
/api/* is slow and uncacheable so caching/failover wins are visible.
"""
import asyncio
import logging
import random

from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

logging.basicConfig(level=logging.INFO, format="%(asctime)s [origin] %(message)s")
log = logging.getLogger("origin")

app = FastAPI(title="Rivet Origin Server")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/static/{name:path}")
async def static_asset(name: str):
    log.info("static %s", name)
    body = f"/* static asset: {name} */\n" + ("x" * 256)
    return Response(
        content=body,
        media_type="text/css",
        headers={"Cache-Control": "max-age=300"},  # cacheable for 5 min
    )


@app.get("/api/data")
async def api_data():
    delay = random.uniform(0.1, 0.5)  # simulate slow backend
    await asyncio.sleep(delay)
    log.info("api/data served in %dms", round(delay * 1000))
    return JSONResponse(
        {"data": "expensive payload", "delay_ms": round(delay * 1000)},
        headers={"Cache-Control": "no-store"},  # never cached
    )
