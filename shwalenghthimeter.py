# Task #3
import re

# Data
data = ['apple', 'banana', 'tractor', 'garik', 'balkon']
vowels = set('aeoiuy')
prefix = 'shwa'
rule3  = r"()"
# rule 4 - add space " " to the end
rule4 = r"()"
# rule 5 - add lenght of original string to the end

for item in data:
    new = item[1:]
    if new[0] in vowels:
    #if set(new[0]).issubset(vowels):
        new1 = prefix + new[1:] 
    else:
        new1 = prefix + new
    result = new1 + ' ' + str(len(item))
    print(item, result)

print("Done")