# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 15:11:03 2017

@author: Igor
"""

unknown_dict = {}
print(unknown_dict.setdefault('key', 'default'))
print(unknown_dict)
# the value assigned by setdefault will not be changed
print(unknown_dict.setdefault('key', 'new_default'))
print(unknown_dict)