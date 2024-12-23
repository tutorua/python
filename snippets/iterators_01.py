# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 15:20:17 2017

@author: Igor
Iterators
"""

collections_map = {
        'mutable' : ['list', 'set', 'dict'],
        'immutable' : ['tuple', 'frosenset']
        }
print (collections_map)

# iteration by the keys
for key in collections_map:
    print(key)

# itteration by the values
for value in collections_map.values():
    print(value)     
    
# itteration by the key-value pairs    
for key, value in collections_map.items():
    print('{} - {}'.format(key, value))    
    
    