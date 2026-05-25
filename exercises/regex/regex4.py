# Exercise: Regex 4
# I AM NOT DONE
#
# Use re.findall with a character-class pattern to collect every
# lowercase ASCII word (only letters a-z) from `text`.
# Store the result in `words`.
#
# Character classes:
#   [a-z]   matches any single lowercase letter
#   [a-z]+  matches a run of one or more lowercase letters
#
# Note: `\w` also matches digits and underscores, so use [a-z]+ here.
# Fix the pattern (replace ???) so that `words` contains only
# lowercase letter runs, ignoring digits and punctuation.

import re

text = "Hello world 123 foo_bar baz!"
words = re.findall("???", text)
