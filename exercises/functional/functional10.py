# Exercise: Functional 10
# I AM NOT DONE
#
# Build a small data-processing pipeline using map, filter, and reduce.
#
# Given a list of raw scores (integers), compute `result` as follows:
#   Step 1 — map:    multiply every score by 2  (use map + lambda)
#   Step 2 — filter: keep only scores > 10      (use filter + lambda)
#   Step 3 — reduce: sum the remaining scores   (use reduce + lambda)
#
# Replace each ??? with the correct lambda.

from functools import reduce

scores = [1, 3, 6, 2, 8, 4]

doubled = list(map(???, scores))
above_ten = list(filter(???, doubled))
result = reduce(???, above_ten)
