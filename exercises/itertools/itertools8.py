# Exercise: Itertools 8
# I AM NOT DONE
#
# Goal: Flatten batches, then collect every pair of adjacent flattened values.

from itertools import pairwise

batches = [[1, 2], [3], [4, 5]]
flattened = [item for batch in batches for item in batch]
adjacent_pairs = list(???)
