# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 15:35:05 2017

@author: Igor
# ordered dictionaries
"""

from collections import OrderedDict

ord_dict = OrderedDict()

for n in range(10):
    ord_dict[n] = str(n)
    
print(ord_dict)


for key in ord_dict:
    print (key)