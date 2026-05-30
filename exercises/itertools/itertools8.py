# Exercise: Itertools 8
# I AM NOT DONE
#
# Goal: Flatten batches, then collect every pair of adjacent flattened values.

try:
    from itertools import pairwise
except ImportError:  # Python < 3.10
    from itertools import tee

    def pairwise(iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

batches = [[1, 2], [3], [4, 5]]
flattened = [item for batch in batches for item in batch]
adjacent_pairs = list(???)
