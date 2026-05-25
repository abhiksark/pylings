# Exercise: Collections 10
# ------------------------
# I AM NOT DONE
#
# Combine what you have learned to analyse a dataset end-to-end.
#
# `log` is a list of (category, value) pairs representing web-server
# requests: category is the endpoint group, value is the response time.
#
# Your tasks:
#   1. Use `defaultdict(list)` named `grouped` to group response times
#      by category.
#   2. Build a `Counter` named `hit_counts` that maps each category to
#      the number of requests it received.
#   3. Store in `top_category` the name of the single most-requested
#      category (the first element returned by `.most_common(1)`).
#   4. Store in `avg_times` a plain dict mapping each category to the
#      average (mean) response time for that category (sum / count).
#      Use regular division — no imports needed.

from collections import defaultdict, Counter

log = [
    ("api",    120), ("web",  45), ("api",   95), ("db",  300),
    ("web",     60), ("api", 110), ("db",   280), ("web",  55),
    ("api",     85), ("db",  310), ("web",   50), ("api", 100),
]

grouped = ???
for category, value in log:
    ???

hit_counts = ???

top_category = ???

avg_times = ???
