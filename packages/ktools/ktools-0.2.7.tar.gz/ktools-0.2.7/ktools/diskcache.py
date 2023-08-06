from pathlib import Path

import diskcache
import ring

cache_dir = Path("~/.diskcache/ktool")
cache_dir.mkdir(parents=True, exist_ok=True)

storage = diskcache.Cache(cache_dir)


def cache(*args, **kwargs):
    return ring.disk(storage, *args, **kwargs)
