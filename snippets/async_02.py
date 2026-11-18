import asyncio
import time
from functools import wraps


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.6f} seconds to execute.")
        return result
    return wrapper

#@time_it
async def task1():
    print("Task 1")
    await asyncio.sleep(3)
    print("Task 1 completed")

#@time_it
async def task2():
    print("Task 2")
    await asyncio.sleep(1)
    print("Task 2 completed")

#@time_it
async def demo():
    print("Process started")
    tasks = [task1(), task2()]
    await asyncio.gather(*tasks)
    print("Process completed")

@time_it
def data_processing_task():
    return sum(i * i for i in range(10_000_000))

# Simply run the function to see its execution time
data_processing_task()

start_time = time.perf_counter()
asyncio.run(demo())
end_time = time.perf_counter()
print(f"Total execution time: {end_time - start_time:.6f} seconds.")

