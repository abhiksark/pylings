# Exercise: Classes 10
# I AM NOT DONE
#
# `Circle.pi` should be a class attribute (shared by all instances),
# not set inside __init__. Move `pi = 3.14159` to be a class-level
# attribute. The `area` method already uses `self.pi` so it will work
# once the attribute is accessible on the instance via the class.
#
# Right now `pi` is only set inside __init__ incorrectly — remove the
# `pi = 3.14159` line from inside __init__ and put it at class level.

class Circle:
    def __init__(self, radius):
        pi = 3.14159        # wrong: local variable, not a class attribute
        self.radius = radius

    def area(self):
        return self.pi * self.radius ** 2


c1 = Circle(1)
c2 = Circle(5)
