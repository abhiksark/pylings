# Exercise: Regex 7
# I AM NOT DONE
#
# Use re.search with a capturing group to extract the area code from
# a US phone number of the form "(NXX) NXX-XXXX".
# Store the three-digit area code string in `area_code`.
#
# Capturing groups:
#   (...)       captures whatever the sub-pattern matches
#   match.group(1) returns the text captured by the first group
#
# The phone number format: (NXX) NXX-XXXX
#   \(   literal open parenthesis
#   \d{3} three digits  ← this is the area code to capture
#   \)   literal close parenthesis
#
# Fix the pattern (replace ???) so that group(1) gives the area code.

import re

phone = "(415) 555-2671"
pattern = "???"
match = re.search(pattern, phone)
area_code = match.group(1)
