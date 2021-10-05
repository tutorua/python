# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 14:39:00 2017

@author: Igor
Simple operations with a dictionary
"""

beatles_map = {
        'Paul' : 'bass',
        'John' : 'guitar',
        'George' : 'Guitar'
}
print (beatles_map)

# add an element
beatles_map['Ringho'] = 'Drums'
print (beatles_map)

# delete an element
del beatles_map['Ringho']
print (beatles_map)

# update an element
beatles_map.update({'John' : 'Guitar'})
print (beatles_map)

# to remove an element by a key and return the value:
print (beatles_map.pop('John'))
print (beatles_map)