import time
from contextlib import contextmanager
from typing import Generator
import redis
from app.config import settings

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

@contextmanager
def redis_lock(key: str, ttl_seconds: int = 15) -> Generator[bool, None, None]:
    token = str(time.time())
    acquired = redis_client.set(key, token, nx=True, ex=ttl_seconds)
    try:
        yield bool(acquired)
    finally:
        # best-effort release
        current = redis_client.get(key)
        if current == token:
            redis_client.delete(key)