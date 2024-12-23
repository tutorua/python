# Python Decorators - Example 3
# https://www.youtube.com/watch?v=r7Dtus7N4pI
# Python Decorators in 15 Minutes

import datetime

def log(func):
    def wrapper(*args, **kwargs):
        with open("logs.txt", "a") as f:
            f.write(f"Called function with {' '.join([str(arg) for arg in args])} at {str(datetime.datetime.now())} \n")
        val = func(*args, **kwargs)
        return val
        
    return wrapper
    
    
@log
def run(a, b, c=9):
    print(a+b+c)
    
    
run(1, 3, c=9)
