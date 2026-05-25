# Exercise: Classes 9
# I AM NOT DONE
#
# Add a `__repr__` method to Color so that repr(c) returns
# "Color(r=<r>, g=<g>, b=<b>)" using the actual values.
# The __str__ is already provided; you only need to add __repr__.

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return f"rgb({self.r}, {self.g}, {self.b})"


c = Color(255, 128, 0)
