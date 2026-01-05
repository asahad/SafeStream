from cachetools import TTLCache
from .settings import settings

cache = TTLCache(maxsize=512, ttl=settings.CACHE_TTL_SECONDS)
seen = TTLCache(maxsize=512, ttl=settings.CACHE_TTL_SECONDS)
