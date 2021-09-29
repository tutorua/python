# Task #1 To write the code to revert the string using 3 different ways

s = "Invert me please"

def invert_string(input):
    output = []
    upb = len(input)
    for i in range(0, upb):
        output.append(input[upb-1-i])
    return ''.join(output)

# straightforward solution
print(invert_string(s)) 


# https://python-scripts.com/reversed
# classic algorithm
def reverse_string3(s):
    chars = list(s)
    for i in range(len(s) // 2):
        tmp = chars[i]
        chars[i] = chars[len(s) - i - 1]
        chars[len(s) - i - 1] = tmp
    return ''.join(chars)

print(reverse_string3(s))


# pythonic solution with slices
# the fastest one, see comparision at  https://python-scripts.com/reversed
print(s[::-1])


# https://www.w3schools.com/python/ref_func_reversed.asp
# The reversed() function returns a reversed iterator object.
print(''.join(reversed(s)))

# The list.reverse() method reverses a List.

