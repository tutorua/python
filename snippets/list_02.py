a = [1, 2, 3]
b = [4, 5, 6]

# Add all elements from list 'b' to the end of list 'a'
c = [item for item in a] + [item for item in b]
print('Combined: ', c)

a.extend(b)
print('Extended: ',  a)

a.append(b)
print('Appended: ', a)

