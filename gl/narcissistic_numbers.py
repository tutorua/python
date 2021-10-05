# Task #2
# https://www.w3resource.com/python-exercises/basic/python-basic-1-exercise-96.php
# added: check if the argument is an integer

def is_narcissistic_number(n):
    str_n = str(n)
    if not str_n.isdigit():
        return False
    
    power = len(str_n)
    return n == sum([int(i) ** power for i in str_n])

print(is_narcissistic_number(7))
print(is_narcissistic_number(371))
print(is_narcissistic_number(122))
print(is_narcissistic_number(4887))