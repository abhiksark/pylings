# Exercise: Classes 8
# I AM NOT DONE
#
# Add a `__str__` method to the Book class so that
# `str(book)` returns the string "Book: <title> by <author>".
# Right now the class has no __str__, so str() returns the default repr.

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author


book = Book("1984", "Orwell")
