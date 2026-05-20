# Exercise: Generators 9
# I AM NOT DONE
#
# Implement the full iterator protocol on `Counter`.
#
# `Counter(stop)` should iterate over 0, 1, 2, ..., stop-1 — just like
# range(stop).  You must implement both:
#   __iter__(self)  — returns self
#   __next__(self)  — returns the next value, or raises StopIteration
#
# The broken version never raises StopIteration, so it loops forever.


class Counter:
    def __init__(self, stop):
        self.stop = stop
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        # Bug: increments forever — add a StopIteration guard.
        value = self.current
        self.current += 1
        return value
