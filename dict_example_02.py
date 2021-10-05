# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 21:04:01 2017

@author: Igor
Dictionary example:
To find the 3 most frequent word in Zen of Python
"""

import this
import operator

zen = """
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
"""

# split the text into the words
zen_map = dict()
for word in zen.split():
    clean_word = word.strip('.-!,').lower()
    if clean_word not in zen_map:
        zen_map[clean_word] = 0
    zen_map[clean_word] += 1
    
print (zen_map)

zen_items = zen_map.items()
word_count_items = sorted(
        zen_items, key=operator.itemgetter(1), reverse=True
)

print (word_count_items[:3])
