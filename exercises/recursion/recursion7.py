# Exercise: Recursion 7
# ---------------------
# I AM NOT DONE
#
# Complete `deep_sum(nested)` so it returns the sum of all numbers in a
# possibly-nested list.  Each element is either an int/float or another
# list.  Base case: empty list returns 0.  Recursive case: if the first
# element is a list, deep_sum it; otherwise treat it as a plain number.
# Add that to deep_sum of the rest.
#
# Example: deep_sum([1, [2, 3], [4, [5]]]) == 15

def deep_sum(nested):
    if not nested:
        return 0
    first = nested[0]
    rest = nested[1:]
    if isinstance(first, list):
        return deep_sum(first) + ???
    return first + deep_sum(rest)
