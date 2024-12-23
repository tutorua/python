# -*- coding: utf-8 -*-
"""
Spyder Editor

Just an example.
Object approach is demonstrated here.
"""
#!usr/bin/env python

class Person(object):
    "A person"
    def __init__(self, name, age):
        self.name = name
        self.age  = age
        
    def greet(self, person):
        print "Hello %s, how are you today?" % (person)
        
John = Person("John", 32)
Erick = Person("Eric", 54)
   
print "John says: ", 
John.greet("Erick")
print "Erick says: ", 
Erick.greet("John")
