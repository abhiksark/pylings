# Exercise: Generators 2
# I AM NOT DONE
#
# `squares(n)` is already a correct generator that yields 1², 2², ..., n².
# Your task: call `squares(5)` and convert the result to a list, storing it
# in the variable `result`.
#
# Hint: a generator object is not a list — wrap it with list().


def squares(n):
    for i in range(1, n + 1):
        yield i * i


# Replace None with the correct expression.
result = None
