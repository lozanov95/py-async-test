import subprocess
from typing import List
import time
import asyncio


def bench(fn):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        res = fn(*args, **kwargs)
        print(f"func[{fn.__name__}] took {time.perf_counter() - start}")
        return res

    return inner


def bench_async(fn):
    async def inner(*args, **kwargs):
        start = time.perf_counter()
        res = await fn(*args, **kwargs)
        print(f"func[{fn.__name__}] took {time.perf_counter() - start}")
        return res

    return inner


class TestAsync:
    def __init__(self) -> None:
        self.N = 10

    def run_subprocess(self, args: List[str]):
        output = subprocess.run(
            args=args,
            capture_output=True,
        )

        return output.stdout.decode()

    def run_test_py(self):
        return self.run_subprocess(
            args=[
                "python",
                "delayme.py",
            ]
        )

    @bench
    def main(self):
        results = [self.run_test_py() for _ in range(self.N)]
        print(results)

    async def run_subprocess_async(self, args: List[str]):
        output = subprocess.run(
            args=args,
            capture_output=True,
        )

        return output.stdout.decode()

    async def run_test_py_async(self):
        return await asyncio.to_thread(
            self.run_subprocess, args=["python", "delayme.py"]
        )

    @bench_async
    async def main_async(self):
        results = await asyncio.gather(
            *[self.run_test_py_async() for _ in range(self.N)],
        )
        print(results)


if __name__ == "__main__":
    asyncio.run(TestAsync().main_async())
    TestAsync().main()
