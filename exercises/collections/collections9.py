# Exercise: Collections 9
# -----------------------
# I AM NOT DONE
#
# Counter supports arithmetic:
#   c1 + c2  — adds counts element-wise
#   c1 - c2  — subtracts counts, dropping non-positive results
#
# Two inventory snapshots are given.
# 1. Store in `combined`  the element-wise sum  of `monday` and `tuesday`.
# 2. Store in `remainder` the result of subtracting `sold` from `combined`.
#    (Only items with a positive remaining count are kept.)

from collections import Counter

monday  = Counter({"apple": 5, "banana": 3, "cherry": 2})
tuesday = Counter({"apple": 2, "banana": 4, "date": 1})
sold    = Counter({"apple": 4, "banana": 5, "cherry": 1})

combined  = ???
remainder = ???
