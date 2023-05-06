import subprocess
from typing import List
import asyncio
from bench import bench_async, bench_sync


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

    async def run_test_py_async(self):
        return await asyncio.to_thread(
            self.run_subprocess, args=["python", "delayme.py"]
        )

    @bench_sync
    def main_sync(self):
        results = [self.run_test_py() for _ in range(self.N)]
        print(results)

    @bench_async
    async def main_async(self):
        results = await asyncio.gather(
            *[self.run_test_py_async() for _ in range(self.N)],
        )
        print(results)


if __name__ == "__main__":
    asyncio.run(TestAsync().main_async())
    TestAsync().main_sync()
