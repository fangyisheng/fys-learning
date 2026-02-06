import asyncio
import time


async def worker(name: str, delay: float) -> str:
    start = time.perf_counter()
    await asyncio.sleep(delay)
    elapsed = time.perf_counter() - start
    return f"{name} finished in {elapsed:.2f}s"


async def main() -> None:
    tasks = [
        asyncio.create_task(worker("A", 1.2)),
        asyncio.create_task(worker("B", 0.6)),
        asyncio.create_task(worker("C", 0.9)),
    ]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
