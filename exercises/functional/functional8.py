# Exercise: Functional 8
# I AM NOT DONE
#
# Use `functools.reduce` to compute the PRODUCT of all numbers in `numbers`.
# `reduce(func, iterable)` applies `func` cumulatively:
#   reduce(f, [a, b, c]) → f(f(a, b), c)
# Replace ??? with a lambda that multiplies two numbers together.

from functools import reduce

numbers = [1, 2, 3, 4, 5]

product = reduce(???, numbers)
