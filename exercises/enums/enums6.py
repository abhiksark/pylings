# Exercise: Enums 6
# I AM NOT DONE
#
# Goal: Give each Direction member a delta tuple and return it from a method.

from enum import Enum

class Direction(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

    def delta(self):
        return ???
