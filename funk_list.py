# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 23:20:14 2017

@author: Igor
Functional programming example
Convert a list of numbers into a list of strings
"""
import random

num_list = []
low = 1
hi = 100

def stringify_list(num_list):
    return list(map(str, num_list))

for i in range(10):
    num_list.append(random.randint(low, hi))

element = stringify_list(num_list)
print(element)
