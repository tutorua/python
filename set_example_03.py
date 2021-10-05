# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 00:26:20 2017

@author: Igor
How many iterations are required to get a repeated number for random generator
"""

import random 

random_set = set()

while True:
    new_number = random.randint(1, 10)
    if new_number in random_set:
        print(new_number)
        break
    random_set.add(new_number)

print(random_set)
print(len(random_set)+1)
