# Python Object Oriented Programming by Joe Marini course example
# Using instance methods and attributes

title1 = "Brave New World"
author1 = "JD Salinger"
pages1 = 234
price1 = 29.95
discount1 = 0.3

title2 = "War and Peace"
author2 = "Leo Tolstoy"
pages2 = 1225
price2 = 39.95
#discount2 = 0

class Book:
    # the "init" function is called when the instance is
    # created and ready to be initialized
    def __init__(self, title, author, pages, price):
        self.title = title
        # TODO: add properties
        self.author =  author
        self.pages = pages
        self.price = price
        self.__secret = "This is a secret attribute"

    # TODO: create instance methods
    def getPrice(self):
        self.price = (self.price * (1 - self._discount) if hasattr(self, "_discount") else self.price)
        return self.price

    def setDiscount(self, amount):
        self._discount = amount


# TODO: create some book instances
b1 = Book(title1, author1, pages1, price1)
b2 = Book(title2, author2, pages2, price2)

# TODO: print the price of book1
print(b1.getPrice())

# TODO: try setting the discount
b1.setDiscount(discount1)
print(b1.getPrice())

# TODO: properties with double underscores are hidden by the interpreter
