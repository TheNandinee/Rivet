"""Per-edge configuration, all overridable via environment variables."""
import os

NODE_NAME = os.getenv("NODE_NAME", "edge-1")
ORIGIN_URL = os.getenv("ORIGIN_URL", "http://origin:9000")

# Cache
DEFAULT_TTL = int(os.getenv("DEFAULT_TTL", "60"))          # seconds
CACHE_MAX_SIZE = int(os.getenv("CACHE_MAX_SIZE", "1000"))  # max keys

# Rate limiting (token bucket)
RATE_LIMIT_CAPACITY = int(os.getenv("RATE_LIMIT_CAPACITY", "100"))  # burst size
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "10"))       # refill window (s)

# Bot detection
BOT_PATH_THRESHOLD = int(os.getenv("BOT_PATH_THRESHOLD", "10"))     # distinct paths
BOT_WINDOW_SECONDS = int(os.getenv("BOT_WINDOW_SECONDS", "5"))      # within this window
