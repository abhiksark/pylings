# Exercise: Dataclasses 5
# I AM NOT DONE
#
# `@dataclass` generates `__init__` automatically from the field
# declarations — you must NOT write your own `__init__`.
#
# Fix `Vector3` by removing the hand-written `__init__` and instead
# declaring three typed fields `x`, `y`, `z` (all `float`).
# The generated __init__ will accept them as positional arguments.
#
# Hint: just add the field declarations and delete the `__init__` method.

from dataclasses import dataclass


@dataclass
class Vector3:
    # Bug: fields are missing; there is a hand-written __init__ below.
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


v = Vector3(1.0, 2.0, 3.0)
