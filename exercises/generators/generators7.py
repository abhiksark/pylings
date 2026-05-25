# Exercise: Generators 7
# I AM NOT DONE
#
# Complete `fibonacci()` so it yields the Fibonacci sequence indefinitely:
# 0, 1, 1, 2, 3, 5, 8, 13, ...
#
# The function should use `yield` inside a loop, updating two variables
# (a, b) each iteration.  The broken version only yields `a` once and stops.


def fibonacci():
    a, b = 0, 1
    # Bug: yields only once instead of looping forever.
    yield a
