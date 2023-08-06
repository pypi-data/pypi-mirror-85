import traceback
from pathlib import Path

import ring

import diskcache

trace = traceback.extract_stack()
filename = Path(trace[-7].filename).name

diskcache.core.DBNAME = f"{filename}.db"

cache_dir = Path("~/.diskcache/ktool").expanduser()
cache_dir.mkdir(parents=True, exist_ok=True)

storage = diskcache.Cache(cache_dir)


def cache(*args, **kwargs):
    return ring.disk(storage, *args, **kwargs)
