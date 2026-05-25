# Exercise: Type Hints 7
# I AM NOT DONE
#
# Annotate the function `apply_twice` using `Callable` from `typing`:
#   - parameter `func` should be annotated as `Callable[[int], int]`
#     (a function that takes one int and returns an int)
#   - parameter `value` should be annotated as `int`
#   - the return type should be `int`
#
# Remember to import `Callable` from `typing`.
#
# The signature should read:
#   def apply_twice(func: Callable[[int], int], value: int) -> int:

from typing import Callable


def apply_twice(func, value):
    return func(func(value))
