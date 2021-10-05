# -*- coding: utf-8 -*-
"""
Spyder Editor

Just an example.
Unit Testing is demonstrated here.
"""
#!usr/bin/env python
import unittest

def divide_by_one(x):
    return x / 1
    
class DivideByOneTest(unittest.TestCase):
    def test(self):
        self.assertEqual(divide_by_one(4), 4)

