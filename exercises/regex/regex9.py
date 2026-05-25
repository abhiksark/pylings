# Exercise: Regex 9
# I AM NOT DONE
#
# Use re.search with named capturing groups to parse a date string of
# the form "YYYY-MM-DD" and extract its parts.
# Store the results in `year`, `month`, and `day` (all strings).
#
# Named groups:
#   (?P<name>...)   captures text and names it `name`
#   match.group("name") retrieves the captured text by name
#
# Fix the pattern (replace ???) so the three named groups
# "year", "month", and "day" each capture the appropriate part.

import re

date_str = "2024-07-15"
pattern = "???"
match = re.search(pattern, date_str)
year = match.group("year")
month = match.group("month")
day = match.group("day")
