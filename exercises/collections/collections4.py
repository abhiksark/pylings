# Exercise: Collections 4
# -----------------------
# I AM NOT DONE
#
# `defaultdict(list)` is great for grouping: every new key starts with
# an empty list so you can append without checking first.
#
# Group the students below by their grade letter.
# `by_grade` should be a `defaultdict(list)` where each key is a grade
# letter and the value is a list of student names with that grade,
# in the order they appear in `students`.

from collections import defaultdict

students = [
    ("Alice", "A"),
    ("Bob", "B"),
    ("Carol", "A"),
    ("Dave", "C"),
    ("Eve", "B"),
    ("Frank", "A"),
]

by_grade = ???
for name, grade in students:
    ???
