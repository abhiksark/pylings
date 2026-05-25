# Exercise: Oop Advanced 10
# I AM NOT DONE
#
# Goal: Implement the abstract area method in Square.

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return ???
