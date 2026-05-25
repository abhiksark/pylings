# Exercise: Classes 4
# I AM NOT DONE
#
# Add a method `area` to the Rectangle class that returns
# `self.width * self.height`. Right now it returns 0.

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return 0


rect = Rectangle(4, 5)
