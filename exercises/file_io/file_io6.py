# Exercise: File IO 6
# I AM NOT DONE
#
# `numbers_path` contains five numbers, one per line:
#   10, 20, 30, 40, 50
#
# Iterate over the lines of the file (using `for line in fh:`) and build
# `total` as the sum of the integer values.
#
# Hint: int(line.strip()) converts a line like "10\n" to the integer 10.

import tempfile

numbers_path = tempfile.mktemp()
with open(numbers_path, "w") as f:
    f.write("10\n20\n30\n40\n50\n")

total = 0
# Iterate over the file's lines and add each integer value to total.
with open(numbers_path) as fh:
    for line in fh:
        total += line   # TODO: convert line to int first (strip whitespace)
