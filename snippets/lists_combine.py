
l1 = [1, 2, 3, 4, 5, 6]
l2 = [7, 8, 9]
# resulting list has to be [1, 7, 2, 8, 3, 9, 4, 5, 6]

def list_mixing(list_long, list_short):
    """
    This function takes two lists and combines them into a new list.
    The elements from the first list are interleaved with the elements from the second list.
    If one list is longer, the remaining elements from the longer list are added at the end.
    """
    a = list_long
    b = list_short

    result = [item for sublist in zip(a,b) for item in sublist]
    # Use map to combine the two lists
    # The None value is used to fill in missing values for shorter lists  
    #result = [item for sublist in map(None, a, b) for item in sublist][:-1]

    # Add the remaining elements from the longer list
    if len(a) > len(b):
        result += a[len(b):]
    else:
        result += b[len(a):]
    return result

# Test the function
print(list_mixing(l1, l2))
# Output: [1, 7, 2, 8, 3, 9, 4, 5, 6]
