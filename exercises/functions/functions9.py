# Exercise: Functions 9
# I AM NOT DONE
#
# Define a function `min_max` that takes a list of numbers and returns a
# tuple of (minimum, maximum).
# Example: min_max([3, 1, 4, 1, 5, 9]) -> (1, 9)
#
# Then unpack the result into two variables `lo` and `hi`.

numbers = [3, 1, 4, 1, 5, 9, 2, 6]

def min_max(nums):
    return min(nums), max(nums)

lo = min_max(numbers)
hi = min_max(numbers)
