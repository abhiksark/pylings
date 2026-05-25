# Exercise: Collections 7
# -----------------------
# I AM NOT DONE
#
# `deque` (double-ended queue) supports O(1) appends and pops from
# BOTH ends — unlike a list, which is O(n) for the left end.
#
# Starting from an empty deque `d`:
#   1. appendleft(1)   — push to the left
#   2. append(2)       — push to the right
#   3. appendleft(0)   — push to the left again
#   4. Store the result of pop()       in `right_val`   (removes from right)
#   5. Store the result of popleft()   in `left_val`    (removes from left)

from collections import deque

d = deque()
???
right_val = ???
left_val = ???
