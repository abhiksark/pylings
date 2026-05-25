# Exercise: Oop Advanced 7
# I AM NOT DONE
#
# Goal: Implement equality for Book objects by ISBN.

class Book:
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return ???
