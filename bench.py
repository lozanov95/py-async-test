import time


def bench_sync(fn):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        res = fn(*args, **kwargs)
        print(f"func[{fn.__name__}] took {time.perf_counter() - start:.3f}s")
        return res

    return inner


def bench_async(fn):
    async def inner(*args, **kwargs):
        start = time.perf_counter()
        res = await fn(*args, **kwargs)
        print(f"func[{fn.__name__}] took {time.perf_counter() - start:.3f}s")
        return res

    return inner
