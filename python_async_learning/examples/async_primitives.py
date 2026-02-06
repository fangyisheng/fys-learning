import asyncio


async def limited_worker(name: str, semaphore: asyncio.Semaphore) -> None:
    async with semaphore:
        print(f"{name} acquired semaphore")
        await asyncio.sleep(0.5)
        print(f"{name} released semaphore")


async def producer(queue: asyncio.Queue[int]) -> None:
    for value in range(3):
        await queue.put(value)
        print(f"Produced {value}")
    await queue.put(-1)


async def consumer(queue: asyncio.Queue[int], event: asyncio.Event) -> None:
    while True:
        item = await queue.get()
        if item == -1:
            queue.task_done()
            event.set()
            break
        print(f"Consumed {item}")
        queue.task_done()


async def main() -> None:
    semaphore = asyncio.Semaphore(2)
    queue: asyncio.Queue[int] = asyncio.Queue()
    done_event = asyncio.Event()

    await asyncio.gather(
        limited_worker("worker-1", semaphore),
        limited_worker("worker-2", semaphore),
        limited_worker("worker-3", semaphore),
        producer(queue),
        consumer(queue, done_event),
    )

    await done_event.wait()
    await queue.join()


if __name__ == "__main__":
    asyncio.run(main())
