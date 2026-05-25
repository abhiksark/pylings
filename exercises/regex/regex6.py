# Exercise: Regex 6
# I AM NOT DONE
#
# Use re.fullmatch (or a pattern with ^ and $) to validate that
# `code` is exactly five uppercase letters followed by exactly three
# digits — nothing more, nothing less.
# Store the boolean result in `is_valid`.
#
# Anchors:
#   ^   start of string
#   $   end of string
#   {n} exactly n repetitions of the preceding element
#   [A-Z] any uppercase letter
#
# Fix the pattern (replace ???).
# Example valid code: "ABCDE123"
# Example invalid: "ABCDE12" (too few digits), "abcde123" (lowercase)

import re

code = "ABCDE123"
pattern = "???"
is_valid = bool(re.fullmatch(pattern, code))
