# Exercise: Collections 3
# -----------------------
# I AM NOT DONE
#
# `defaultdict(int)` is handy for counting: accessing a missing key
# automatically starts its count at 0.
#
# Use a `defaultdict(int)` to count how many times each character
# appears in `text`. Store the defaultdict in `char_counts`.
# Do NOT use Counter — iterate over the string and increment manually.

from collections import defaultdict

text = "mississippi"
char_counts = ???
for ch in text:
    ???
