# Exercise: Oop Advanced 8
# I AM NOT DONE
#
# Goal: Add a classmethod constructor that parses "x,y" text.

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_text(cls, text):
        x_text, y_text = text.split(",")
        return ???
