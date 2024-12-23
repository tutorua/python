# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 20:25:12 2016

@author: Igor

Python has 3 methods used for string formatting:
- оператор %  
- строковый метод format()  
- f-строки

For details see also https://pyformat.info/
"""
name = 'James'
surname = 'Bond'
age = 64
# operator % remained for compatibility and might look redundant
print('My name is %s' % name)
print('I am %d years old' % age)
print('Numerical value for %s is %04.2f or %e' % ('Pi', 3.14, 3.14))
print()

# method format() might look redundant
result = 'My name is {}, {} {}'.format(surname, name, surname)
print(result)
result = 'My name is {1}, {0} {1}'.format(name, surname)
print(result)
result = 'My name is {surname}, {0} {surname}'.format(name, surname='Bond')
print(result)
print()

# the suggested modern way is called f-string (possibly like G-string)
data = {'first': 'Hodor', 'last': 'Hodor!'}
print('{first} {last}'.format(**data))
result = f'My name is {surname}, {name.upper()} {surname.upper()}'
print(result)
print(f'My name is {"Bond"}, {"James"} {"Bond"}')
print(f'{age}')
print(f'{{age}}')
print(f'{{{age}}}')
print(f'{{{{age}}}}')
print(f'{{{{{age}}}}}')
print(f'\\a\\b\\f\\n\\r\\t\\v')
print(fr'\a\b\f\n\r\t\v')
# does not work works for Python <= 3.11
#print(f'My name is {'Bond'}, {'James'} {'Bond'}')
# print(f'{"\n".join(["James", "Bond"])}')
print()


hello = 'hello'   # String literals can use single quotes
world = "world"   # or double quotes; it does not matter.
print(hello)       # Prints "hello"
print(len(hello))  # String length; prints "5"
hw = hello + ' ' + world  # String concatenation
print(hw)  # prints "hello world"
hw12 = '%s %s %d' % (hello, world, 12)  # sprintf style string formatting
print(hw12)  # prints "hello world 12"


s = "hello"
print(s.capitalize())  # Capitalize a string; prints "Hello"
print(s.upper())       # Convert a string to uppercase; prints "HELLO"
print(s.rjust(7))      # Right-justify a string, padding with spaces; prints "  hello"
print(s.center(7))     # Center a string, padding with spaces; prints " hello "
print(s.replace('l', '(ell)'))  # Replace all instances of one substring with another;
                               # prints "he(ell)(ell)o"
print('  world '.strip())  # Strip leading and trailing whitespace; prints "world"
