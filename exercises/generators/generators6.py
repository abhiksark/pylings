# Exercise: Generators 6
# I AM NOT DONE
#
# `natural_numbers()` must be an infinite generator that yields 1, 2, 3, 4, ...
# without ever stopping.
#
# `first_ten` should be the list [1, 2, 3, ..., 10] — take only the first 10
# values from the infinite generator using itertools.islice.
#
# Hint: import itertools, then use itertools.islice(natural_numbers(), 10).

import itertools


def natural_numbers():
    # Bug: this yields nothing — make it yield 1, 2, 3, ... forever.
    return


first_ten = list(itertools.islice(natural_numbers(), 10))
