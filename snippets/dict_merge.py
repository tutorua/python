# merge two dictionaries with merge operator 

first_dict = {"kelly": 23, "Derick": 14, "John": 7}
second_dict = {"Ravi": 45, "Mpho": 67}

combined_dict1 = first_dict | second_dict
print(combined_dict1)

# {'kelly': 23, 'Derick': 14, 'John': 7, 'Ravi': 45, 'Mpho': 67}

# merge two dictionaries with unpacking operator
third_dict = {"kelly": 23, "Derick": 14, "John": 7}
fourth_dict = {"Ravi": 45, "Mpho": 67}

combined_dict2 = {**third_dict, **fourth_dict}
print(combined_dict2)

# {'kelly': 23, 'Derick': 14, 'John': 7, 'Ravi': 45, 'Mpho': 67} 
