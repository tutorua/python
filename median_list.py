# -*- coding: utf-8 -*-
"""
Spyder Editor

This program returns the median of a list.
Sort list in ascending order/
Return the median value. 
In a case of even number returns the average of the two adjacent elements. 

Something is definitely wrong with the algorithm.  Check for elements = 2 
The result is wrong.
For number of elements = 1 IndexError occurs!
"""

import random
import statistics

elements = 20
min_value = 10
max_value = 30

my_list = []

for _ in range(elements):
    my_list.append(random.randint(min_value, max_value))
    
print (my_list)
my_list.sort()
print (my_list)
half_size = len(my_list) // 2
print (half_size)

if half_size % 2 == 1:
    median = my_list[half_size]
else: 
    print(my_list[half_size-1])
    print(my_list[half_size+1])
    median = sum(my_list[half_size-1 : half_size+1])/2
    
print ("Median value of the list: " )
print (median)

# check our result by comparing with the standard module
st_median = statistics.median(my_list)
print (st_median)

