# Exercise: Decorators 8
# I AM NOT DONE
#
# A decorator factory is a function that RETURNS a decorator.
# `repeat(n)` should return a decorator that calls the wrapped function
# n times and returns the last result.
#
# Complete the two missing inner functions so that repeat(n) works correctly.

import functools


def repeat(n):
    # return a decorator here
    pass


@repeat(3)
def say(word):
    return word


@repeat(1)
def identity(x):
    return x
