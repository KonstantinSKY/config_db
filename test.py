import asyncio

import asyncio

async def add(a: int, b: int):
    return a + b

async def get_result():
    inputs = [(4, 5), (6, 6), (7, 8), (9, 4)]

    tasks = [asyncio.create_task(add(a, b)) for a, b in inputs]
    result = asyncio.gather(*tasks)
    print("Result: ")
    print(await result)

asyncio.run(get_result())