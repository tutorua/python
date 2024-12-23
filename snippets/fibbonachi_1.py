# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:07:16 2016

@author: Igor
"""
# 1 1 2 3 5 8 13 21
# 0 1 2 3 4 5  6  7
def fibonacci(number):
    prev = 0
    next = 1
    fib = 1
    if (number < 2):
        fib = 1
    else: 
        for i in (range(number-1)):
            fib = prev + next
            prev = next
            next = fib 
    return fib
    
for i in range(1,10):
    print(fibonacci(i))