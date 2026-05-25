# Exercise: Recursion 4
# ---------------------
# I AM NOT DONE
#
# Complete `count_items(lst)` so it returns the number of elements in
# `lst` using recursion — without calling `len()`.  Base case: empty
# list has length 0.  Recursive case: 1 + count_items of the tail.

def count_items(lst):
    if not lst:
        return ???
    return 1 + count_items(lst[1:])
