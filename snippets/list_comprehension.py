# remove all 2 from the list

items = [1, 2, 2, 3, 4]

items = [x for x in items if x != 2]

print(items) # [1, 3, 4]
