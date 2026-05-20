# Exercise: Decorators 9
# I AM NOT DONE
#
# Decorators can be stacked: the one closest to `def` is applied first,
# then the outer one wraps that result.
#
# Given the two decorators below, apply BOTH to `get_value` using the `@`
# syntax so that calling get_value() returns "[B][A]42".
#
# Stack order matters: figure out which decorator goes on top.


def add_a(func):
    def wrapper():
        return "[A]" + func()
    return wrapper


def add_b(func):
    def wrapper():
        return "[B]" + func()
    return wrapper


def get_value():
    return "42"
