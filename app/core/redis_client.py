from typing import Optional

import redis

from app.config import settings

_redis: Optional[redis.Redis] = None


def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def set_token_expiry(key: str, value: str, ttl_seconds: int) -> None:
    """Store token or session key in Redis with TTL (e.g. for revocation or expiry tracking)."""
    r = get_redis()
    r.setex(key, ttl_seconds, value)
