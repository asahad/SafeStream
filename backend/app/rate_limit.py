import time
from cachetools import TTLCache
from .settings import settings

_last_call = TTLCache(maxsize=2048, ttl=3600)

def enforce_min_interval(ip: str):
    now = time.time()
    last = _last_call.get(ip)
    if last and now - last < settings.MIN_SECONDS_BETWEEN_CALLS:
        wait = int(settings.MIN_SECONDS_BETWEEN_CALLS - (now - last))
        raise RuntimeError(f"Rate limit: wait {wait}s")
    _last_call[ip] = now
