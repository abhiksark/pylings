# Exercise: Oop Advanced 3
# I AM NOT DONE
#
# Goal: Use polymorphism by calling area on every shape.

class Square:
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

def total_area(shapes):
    return ???
