# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 19:45:33 2016

@author: Igor
"""

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    print len(arr) / 2
    pivot = arr[len(arr) / 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
    
print quicksort([3,6,8,10,1,2,1])