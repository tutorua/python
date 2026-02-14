empty_list = [] # Create an empty list
# Add elements to the list
empty_list.append('Michael Jackson')
empty_list.append(10.2)
empty_list.extend(['pop', 10])
print(empty_list) 
# Output: ['Michael Jackson', 10.2, 'pop', 10]
# Add a list to the list
empty_list.append(['rock', 'star'])
print(empty_list)
# Output: ['Michael Jackson', 10.2, 'pop', 10, ['rock', 'star']]
empty_list.insert(0, 'pop') # Insert 'pop' at index 0
print(empty_list)  
# Output: ['pop', 'Michael Jackson', 10.2, 'pop', 10, ['rock', 'star']]
del empty_list[3] # Delete the element at index 3
print(empty_list)
# Output: ['pop', 'Michael Jackson', 10.2, 10, ['rock', 'star']]
# Delete the last element       
del empty_list[-1] # Delete the last element
print(empty_list)
# Output: ['pop', 'Michael Jackson', 10.2, 10]
# Delete the first element  
del empty_list[0] # Delete the first element
print(empty_list)
# Output: ['Michael Jackson', 10.2, 10]
# Delete the last element
del empty_list[-1] # Delete the last element
print(empty_list)       
# Output: ['Michael Jackson', 10.2]


# Create a list with mixed data types
data = ['Dave', 42, True] 
print ("Dave" in data) # Check if "Dave" is in the list
# Output: True

s = 'This is a string data.'
s_list = list(s)
# Convert the string to a list of characters
# Output: ['T', 'h', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', 's', 't', 'r', 'i', 'n', 'g', ' ', 'd', 'a', 't', 'a', '.']
print(s_list)
# Convert the string to a list of words
# Note: The split() method splits the string at whitespace by default.
# Output: ['This', 'is', 'a', 'string', 'data.']
s_list = s.split()
print(s_list)

