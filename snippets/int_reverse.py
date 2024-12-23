number = 12345  # Example number
reversed_number = 0

while number > 0:
    digit = number % 10  # Extract the last digit
    reversed_number = reversed_number * 10 + digit  # Build the reversed number
    number //= 10  # Remove the last digit

print("Reversed Number:", reversed_number)