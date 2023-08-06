import diskcache

storage = diskcache.Cache("~/.diskcache/ktool")


def cache(*args, **kwargs):
    return storage.memoize(*args, **kwargs)
