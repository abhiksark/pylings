# Exercise: Regex 2
# I AM NOT DONE
#
# Use re.search to find the word "python" anywhere inside `text`.
# Store the result (a match object or None) in `result`.
#
# Unlike re.match, re.search scans through the whole string looking for
# the first location where the pattern matches.
#
# Fix the pattern so that `result` is not None for the given `text`.

import re

text = "I love python programming"
pattern = "???"
result = re.search(pattern, text)
