# Exercise: Regex 8
# I AM NOT DONE
#
# Use re.sub to censor every occurrence of a bad word in `text` by
# replacing it with "***". The bad words are: "spam" and "junk".
# Store the cleaned string in `clean`.
#
# re.sub(pattern, replacement, string) returns a new string with all
# matches replaced by `replacement`.
#
# Hint: the pipe character | means "or" in a regex:  spam|junk
#
# Fix the pattern (replace ???).

import re

text = "This email is full of spam and junk, total spam!"
pattern = "???"
clean = re.sub(pattern, "***", text)
