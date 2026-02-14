# the idea based on the ariticle: 
# the goal is to emulate multitasking by rotating tasks
# https://medium.com/swlh/understanding-multitasking-in-python-3-using-generators-3f2d4f3c8a8e
import time 
import random
from collections import deque
from datetime import datetime
from pathlib import Path
import os
import shutil
import threading
from queue import Queue


def task(name, n):
    for i in range(n):
        print(f"Task {name}: step {i+1}/{n}")
        time.sleep(random.uniform(0.1, 0.5))  # Simulate work
        yield


def rotate_tasks(tasks):
    task_queue = deque(tasks)
    while task_queue:
        current_task = task_queue.popleft()
        try:
            next(current_task)
            task_queue.append(current_task)  # Re-add the task if not done
        except StopIteration:
            print(f"Task completed and removed from queue.")
        time.sleep(0.1)  # Small delay to simulate time slicing between tasks
    print("All tasks completed.")


if __name__ == "__main__":
    tasks = [task("A", 5), task("B", 3), task("C", 4)]
    rotate_tasks(tasks)


now = '{:%Y-%m-%d %H:%M}'.format(datetime(2001, 2, 3, 4, 5))
print(now)
