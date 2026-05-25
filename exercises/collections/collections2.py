# Exercise: Collections 2
# -----------------------
# I AM NOT DONE
#
# `Counter.most_common(n)` returns the n most frequent elements as a list
# of (element, count) pairs, highest count first.
#
# Given `votes`, build a Counter called `tally` and then store in
# `top2` the two most common candidates (call `.most_common(2)`).

from collections import Counter

votes = [
    "Alice", "Bob", "Alice", "Carol", "Bob", "Alice",
    "Carol", "Bob", "Alice", "Carol",
]
tally = Counter(votes)
top2 = ???
