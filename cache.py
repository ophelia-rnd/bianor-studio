import os
from flask_caching import Cache

import shutil

timeout = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))
cache_dir = os.getenv("CACHE_DIR", ".bianor_cache")

cache = Cache(
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": cache_dir,
        "CACHE_DEFAULT_TIMEOUT": timeout,
    }
)


def clear_cache():
    """Clears the configured CACHE_DIR."""
    shutil.rmtree(cache_dir, ignore_errors=True)
    os.makedirs(cache_dir, exist_ok=True)
