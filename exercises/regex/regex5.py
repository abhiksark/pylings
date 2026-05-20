# Exercise: Regex 5
# I AM NOT DONE
#
# Use re.findall to find all tokens that look like version numbers:
# one or more digits, a literal dot, one or more digits
# (e.g. "3.10", "1.0", "2.7").
# Store the result in `versions`.
#
# Quantifier reminder:
#   +     one or more of the preceding element
#   \d    any digit  (same as [0-9])
#   \.    a literal dot (dot without backslash means "any character")
#
# Fix the pattern (replace ???) to capture version-like tokens.

import re

text = "requires python 3.10 or 2.7, not 1.x or 42"
versions = re.findall("???", text)
