import subprocess
from typing import List
import asyncio
from bench import bench_async, bench_sync


class TestBase:
    def __init__(self, n: int) -> None:
        self.N = n

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


class TestSync(TestBase):
    def run_test_py(self):
        return self.run_subprocess(
            args=[
                "python",
                "delayme.py",
            ]
        )

    @bench_sync
    def main(self):
        results = [self.run_test_py() for _ in range(self.N)]
        print(results)


class TestAsync(TestBase):
    async def run_test(self):
        return await asyncio.to_thread(
            self.run_subprocess, args=["python", "delayme.py"]
        )

    @bench_async
    async def main(self):
        results = await asyncio.gather(
            *[self.run_test() for _ in range(self.N)],
        )
        print(results)


if __name__ == "__main__":
    n = 10
    asyncio.run(TestAsync(n).main())
    TestSync(n).main()
