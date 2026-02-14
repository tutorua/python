# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 22:30:20 2017

@author: Igor
"""

odd_set = set()
even_set = set()

for number in range(10):
    if number % 2:
        odd_set.add(number)
    else:
        even_set.add(number)
        
print(odd_set)
print(even_set)

union_set = odd_set | even_set
print(union_set)     

union_set = odd_set.union(even_set)
print(union_set)  


difference_set = odd_set - even_set        
print(difference_set) 

difference_set = union_set.difference(odd_set)
print(difference_set) 

even_set.remove(2)
print(even_set)

frozen = frozenset(['one', 'three', 'four'])
print(frozen)
# AttributeError: 'frozenset' object has no attribute 'add'
# frozen.add('two')
# print(frozen)

set_a: set[int] = {1, 2, 3, 4, 5}
set_b: set[int] = {4, 5, 6, 7, 8}
print(set_a & set_b) # common elements - intersection
print(set_a ^ set_b) # unique elements 