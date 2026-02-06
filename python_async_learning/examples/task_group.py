import asyncio
import random


async def fetch_item(item_id: int) -> str:
    await asyncio.sleep(random.uniform(0.2, 0.8))
    return f"item-{item_id}"


async def main() -> None:
    results: list[str] = []
    async with asyncio.TaskGroup() as tg:
        for item_id in range(1, 6):
            tg.create_task(collect_result(item_id, results))
    print("Results:", ", ".join(results))


async def collect_result(item_id: int, results: list[str]) -> None:
    item = await fetch_item(item_id)
    results.append(item)


if __name__ == "__main__":
    asyncio.run(main())
