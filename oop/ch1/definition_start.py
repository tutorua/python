# Python Object Oriented Programming by Joe Marini course example
# Basic class definitions

title1 = "Brave New World"
title2 = "War and Peace"

# TODO: create a basic class
class Book:
    def __init__(self, title):
        self.title = title
    

# TODO: create instances of the class
b1 = Book(title1)
b2 = Book(title2)

# TODO: print the class and property
print(b1)
print(b1.title)
