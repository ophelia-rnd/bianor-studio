import os
from flask_caching import Cache

timeout = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))
cache_dir = os.getenv("CACHE_DIR", ".bianor_cache")

cache = Cache(
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": cache_dir,
        "CACHE_DEFAULT_TIMEOUT": timeout,
    }
)
