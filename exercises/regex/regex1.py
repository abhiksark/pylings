# Exercise: Regex 1
# I AM NOT DONE
#
# Use re.match to check whether `text` starts with the word "hello".
# Store the result (a match object or None) in `result`.
#
# re.match(pattern, string) returns a match object if the beginning of
# `string` matches `pattern`, otherwise None.
#
# Fix the pattern so that `result` is not None for the given `text`.

import re

text = "hello world"
pattern = "???"
result = re.match(pattern, text)
