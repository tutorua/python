# Use append to add elements to list
L = [ "Michael Jackson", 10.2]
L.append(['pop', 10])
print(L)

# Output: ['Michael Jackson', 10.2, ['pop', 10]]

# To add an element:
Shopping_list.append("Football")


# Use extend to add elements to list
L = [ "Michael Jackson", 10.2]
L.extend(['pop', 10])
print(L)

# Output: ['Michael Jackson', 10.2, 'pop', 10]
# Do not forget to use squared braces: 
Shopping_list.extend(["Football"])
print(Shopping_list)


# Change the element based on the index
A = ["disco", 10, 1.2]
print('Before change:', A)
A[0] = 'hard rock'
print('After change:', A)

# Output:
# Before change: ['disco', 10, 1.2]
# After change: ['hard rock', 10, 1.2]


# Delete the element based on the index
print('Before change:', A)
del(A[0])
print('After change:', A)

# Output:
# Before change: ['hard rock', 10, 1.2]
# After change: [10, 1.2]


# Split the string, default is by space
'hard rock'.split()

# Output: ['hard', 'rock']


# Split the string by a delimeter (e.g. comma)
'A,B,C,D'.split(',')

# Output: ['A', 'B', 'C', 'D']


# Copy (copy by reference) the list A. Changes in any list will affect another.
A = ["hard rock", 10, 1.2]
B = A
print('A:', A)
print('B:', B)

# Output: 
# A: ['hard rock', 10, 1.2]
# B: ['hard rock', 10, 1.2]

# Examine the copy by reference. Changes in any list will affect another.
print('B[0]:', B[0])
A[0] = "banana"
print('B[0]:', B[0])

# Output: 
# B[0]: hard rock
# B[0]: banana


# Clone (clone by value) the list A
B = A[:]
print(B)
# Output:  ['banana', 10, 1.2]

# Examine the cloning
print('B[0]:', B[0])
A[0] = "hard rock"
print('B[0]:', B[0])

# Output:  
# B[0]: banana
# B[0]: banana








