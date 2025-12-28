import time

# In-memory cache
_CACHE = {}

# Example key:
# ("RELIANCE.NS", "DAILY") → { "data": {...}, "ts": 123456 }

def set_cache(key, value):
    _CACHE[key] = {
        "data": value,
        "ts": time.time()
    }

def get_cache(key):
    return _CACHE.get(key)

def delete_cache(key):
    _CACHE.pop(key, None)

def clear_cache():
    _CACHE.clear()

def clean_expired(ttl_seconds: int):
    now = time.time()
    expired = [
        k for k, v in _CACHE.items()
        if now - v["ts"] > ttl_seconds
    ]
    for k in expired:
        del _CACHE[k]
