import asyncio
from typing import List, Optional, Awaitable

import aiohttp


async def semaphore_wrapper(coroutine: Awaitable, sem: asyncio.Semaphore):
    async with sem:
        return await coroutine

async def fetch_one(url: str, session: aiohttp.ClientSession):
    async with session.get(url) as resp:
        return await resp.json()


async def fetch_all(urls: List[str], limit: int) -> List[Optional[str]]:
    sem = asyncio.Semaphore(limit)
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[semaphore_wrapper(fetch_one(url, session), sem) for url in urls]
        )
        print(f"{results=}")
    return results

async def main() -> None:
    urls = [
        "https://jsonplaceholder.typicode.com/todos/1",
        "https://jsonplaceholder.typicode.com/todos/2",
        "https://jsonplaceholder.typicode.com/todos/3",
        "https://jsonplaceholder.typicode.com/todos/4",
        "https://jsonplaceholder.typicode.com/todos/5",
        "https://jsonplaceholder.typicode.com/todos/6",
        "https://jsonplaceholder.typicode.com/todos/7",
        "https://jsonplaceholder.typicode.com/todos/8",
        "https://jsonplaceholder.typicode.com/todos/9",
        "https://jsonplaceholder.typicode.com/todos/10",
    ]

    limit = 2

    result = await fetch_all(urls,limit)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

