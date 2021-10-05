# Task #3
import re

# Data
data = ['apple', 'banana', 'tractor', 'garik', 'balkon']
vowels = set('aeoiuy')
prefix = 'shwa'

for item in data:
    new = item[1:]
    if new[0] in vowels:
        new1 = prefix + new[1:] 
    else:
        new1 = prefix + new
    result = new1 + ' ' + str(len(item))
    print(item, result)

print("Done")