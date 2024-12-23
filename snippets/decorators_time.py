# Python Decorators - Example 2
# https://www.youtube.com/watch?v=r7Dtus7N4pI
# Python Decorators in 15 Minutes

import time

def timer(func):
    def wrapper():
        before = time.time()
        func()
        print("Function took:", time.time() - before, "seconds")
        print(f"Function took: {time.time() - before} seconds")
        
    return wrapper
    

@timer
def run():
    time.sleep(2)
    
    
run()
        