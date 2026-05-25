# Exercise: Regex 3
# I AM NOT DONE
#
# Use re.findall to collect every run of digits in `text` as a list
# of strings. Store the result in `numbers`.
#
# re.findall(pattern, string) returns a list of all non-overlapping
# matches of `pattern` in `string`.
#
# The pattern `\d+` matches one or more digit characters.
# Fix the pattern (replace ???) so that `numbers` holds all digit runs.

import re

text = "order 12 has 3 items and 450 points"
numbers = re.findall("???", text)
