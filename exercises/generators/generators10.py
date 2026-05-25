# Exercise: Generators 10
# I AM NOT DONE
#
# Complete `running_total(numbers)` — a streaming generator that takes any
# iterable of numbers and yields the cumulative (running) sum after each item.
#
# Example: running_total([1, 2, 3, 4]) → 1, 3, 6, 10
#
# The broken version yields each raw number unchanged instead of accumulating.


def running_total(numbers):
    total = 0
    for n in numbers:
        # Bug: yields n instead of the accumulated total.
        yield n
