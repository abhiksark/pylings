# Exercise: Generators 5
# I AM NOT DONE
#
# Use `next()` to pull individual values from a generator one at a time.
#
# `letters` is a generator that yields 'a', 'b', 'c'.
# Pull the first value into `first`, the second into `second`, and
# the third into `third` — each with a separate call to next().
#
# Do NOT convert the whole generator to a list.


def letters():
    yield "a"
    yield "b"
    yield "c"


gen = letters()

# Replace each None with a next() call on gen.
first = None
second = None
third = None
