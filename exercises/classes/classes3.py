# Exercise: Classes 3
# I AM NOT DONE
#
# The Point class should store both `x` and `y` as instance attributes
# in its __init__. Right now only `x` is stored. Add `self.y = y`.

class Point:
    def __init__(self, x, y):
        self.x = x
        # also store y on the instance


p = Point(3, 7)
