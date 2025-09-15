import json
from typing import Optional, Any, Dict
import pickle
from datetime import datetime, timedelta

from app.core.database import redis_client
from app.core.config import settings


def get_cache_key(prefix: str, **kwargs) -> str:
    """
    Generate a cache key from a prefix and kwargs
    """
    key_parts = [prefix]
    for k, v in sorted(kwargs.items()):
        if v is not None:
            key_parts.append(f"{k}:{v}")
    return ":".join(key_parts)


def get_cached_data(key: str) -> Optional[Any]:
    """
    Get data from cache
    """
    try:
        cached = redis_client.get(key)
        if cached:
            return pickle.loads(cached)
        return None
    except Exception as e:
        print(f"Error getting cache: {str(e)}")
        return None


def set_cached_data(key: str, data: Any, ttl: int = None) -> bool:
    """
    Set data in cache
    """
    try:
        ttl = ttl or settings.CACHE_TTL
        serialized = pickle.dumps(data)
        redis_client.setex(key, ttl, serialized)
        return True
    except Exception as e:
        print(f"Error setting cache: {str(e)}")
        return False


def invalidate_cache(key: str) -> bool:
    """
    Invalidate cache for a specific key
    """
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        print(f"Error invalidating cache: {str(e)}")
        return False


def invalidate_cache_pattern(pattern: str) -> bool:
    """
    Invalidate cache for all keys matching a pattern
    """
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
        return True
    except Exception as e:
        print(f"Error invalidating cache pattern: {str(e)}")
        return False