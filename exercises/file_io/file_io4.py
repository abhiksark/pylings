# Exercise: File IO 4
# I AM NOT DONE
#
# `poem_path` already contains three lines:
#   "roses are red\n"
#   "violets are blue\n"
#   "python is great\n"
#
# Read ALL lines from the file and store them in the variable `lines`
# as a list of strings (newlines included, as .readlines() returns them).
#
# Hint: open(path).readlines() returns a list of lines.

import tempfile

poem_path = tempfile.mktemp()
with open(poem_path, "w") as f:
    f.write("roses are red\nviolets are blue\npython is great\n")

# Read all lines into `lines`.
lines = open(poem_path).read()   # TODO: use .readlines() instead of .read()
