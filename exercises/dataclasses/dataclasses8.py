# Exercise: Dataclasses 8
# I AM NOT DONE
#
# Challenge: add a method to a dataclass.
#
# `Rectangle` has two float fields, `width` and `height`.
# Add two methods:
#   * `area(self) -> float`  — returns width * height
#   * `perimeter(self) -> float` — returns 2 * (width + height)
#
# The class already has the @dataclass decorator and the field
# declarations.  Only the method bodies are missing — fill them in.

from dataclasses import dataclass


@dataclass
class Rectangle:
    width: float
    height: float

    def area(self) -> float:
        pass  # Bug: return the correct value

    def perimeter(self) -> float:
        pass  # Bug: return the correct value


rect = Rectangle(4.0, 3.0)
square = Rectangle(5.0, 5.0)
