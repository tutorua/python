# -*- coding: utf-8 -*-
"""
Spyder Editor

Just an example.
Functional approach is demonstrated here.
"""
#!usr/bin/env python

myList = [i for i in range(1, 20)] 

# print even numbers
print filter(lambda x: x%2 == 0, myList)
# print odd numbers
print filter(lambda x: x%2 == 1, myList)
