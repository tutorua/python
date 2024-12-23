# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 10:50:14 2017

@author: Igor
Dictionary demo
"""

my_dict = {}
new_dict = dict()

collections_map = {
        'mutable' : ['list', 'set', 'dict'],
        'immutable' : ['tuple', 'frosenset']
        }

print (collections_map)
print (collections_map['immutable'])

# not to get an error if a key does nt exists:
print (collections_map.get('reverse', 'the key reverse not found'))

# To check if the key is present:
print ('mutable' in collections_map)