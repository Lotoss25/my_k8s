import asyncio
import time

async def fetch_data(name, seconds):
    print(f"{name}: починаю...")
    await asyncio.sleep(seconds)
    print(f"{name}: готово! ({seconds}с)")
    return f"результат від {name}"


# async def run_sync():
#     start = time.time()
#     await fetch_data("Скелет-1", 2)
#     await fetch_data("Скелет-2", 2)
#     await fetch_data("Скелет-3", 2)
#     print(f"Загалом {time.time() - start:.1f}c")

async def run_async():
    start = time.time()
    results = await asyncio.gather(
        fetch_data("Скелет-1", 1),
        fetch_data("Скелет-2", 2),
        fetch_data("Скелет-3", 3)
    )
    print(f"Загалом {time.time() - start:.1f}c")
    print(results)


asyncio.run(run_async())