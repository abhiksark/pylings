# Exercise: Dataclasses 2
# I AM NOT DONE
#
# Construct an instance of `Color` and read its fields.
# Set `red=255`, `green=128`, `blue=0` when creating `orange`.
# Then complete the `describe` call so it returns the string
# "R=255 G=128 B=0".
#
# Hint: fields are plain attributes — use dot notation to read them.

from dataclasses import dataclass


@dataclass
class Color:
    red: int
    green: int
    blue: int


orange = Color(0, 0, 0)  # Bug: wrong values — use 255, 128, 0

description = f"R=??? G=??? B=???"  # Bug: replace ??? with the field values
