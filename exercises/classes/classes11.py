# Exercise: Classes 11
# I AM NOT DONE
#
# Add a class method `from_string` to Temperature that parses a string
# like "36.6C" and returns a new Temperature instance with the numeric
# value. For example, Temperature.from_string("100C") should return
# Temperature(100.0).
#
# The method signature is:
#   @classmethod
#   def from_string(cls, s):
#       ...
#
# Hint: float(s[:-1]) strips the trailing "C" and converts to float.

class Temperature:
    def __init__(self, degrees):
        self.degrees = degrees

    # Add from_string here


t = Temperature.from_string("36.6C")
boiling = Temperature.from_string("100C")
