# the recepie from official documentation
# print the first n fibonacci numbers

def fib(n):
    a, b = 0, 1
    for i in range(n):
        print(i)
        a, b = b, a+b
    return b
    
print(fib(5))