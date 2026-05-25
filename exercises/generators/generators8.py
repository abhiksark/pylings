# Exercise: Generators 8
# I AM NOT DONE
#
# Make `Countdown` iterable by implementing `__iter__`.
#
# `Countdown(n)` should iterate from n down to 1 (inclusive).
# The class already stores `self.start`.  Add an `__iter__` method that
# returns a generator (use `yield` inside it) — do NOT add `__next__`.
#
# Example: list(Countdown(3)) == [3, 2, 1]


class Countdown:
    def __init__(self, start):
        self.start = start

    # Bug: __iter__ is missing — add it so the class is iterable.
