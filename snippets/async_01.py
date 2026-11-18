import asyncio

async def demo():
    print("Hello")
    await asyncio.sleep(1)
    print("World") 

asyncio.run(demo())
