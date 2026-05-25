# Exercise: Testing 10
# I AM NOT DONE
#
# Robust tests include *edge cases*: empty input, zero, negatives, and
# boundary values — the inputs most likely to expose bugs.
#
# Complete `test_sum_list` to cover ALL of the following edge cases for
# `sum_list(numbers)`:
#   sum_list([])          == 0         (empty list)
#   sum_list([0])         == 0         (single zero)
#   sum_list([-1, -2])    == -3        (all negatives)
#   sum_list([1, -1])     == 0         (cancellation)
#   sum_list([1, 2, 3])   == 6         (normal case)

def sum_list(numbers):
    return sum(numbers)


def test_sum_list():
    # write five assertions covering the edge cases above
    pass
