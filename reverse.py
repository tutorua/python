# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 00:46:02 2017

@author: Igor
reverse list (string) 
"""

init_string = '1234567890'
print(init_string) 
print(list(init_string))

reversed_string = []
reversed_string.append(list(init_string).pop())
print(reversed_string)

print(''.join(reversed(init_string))) 
print(init_string[::-1])


