# Exercise: Generators 3
# I AM NOT DONE
#
# `evens_up_to(n)` should be a generator that yields every even number
# from 2 up to and including n (if n is even), e.g. evens_up_to(8) → 2 4 6 8.
#
# Use a for loop over range and yield only the even numbers.
# The collected list is built by iterating the generator with a for loop.


def evens_up_to(n):
    for i in range(1, n + 1):
        # yield only when i is even
        pass


collected = []
for value in evens_up_to(8):
    collected.append(value)
