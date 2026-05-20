# Exercise: File IO 5
# I AM NOT DONE
#
# `journal_path` already has the line "day 1: sunny\n" written to it.
# Open the same file in APPEND mode ("a") and write "day 2: rainy\n"
# so that both lines are present in the file.
#
# Append mode adds content after what already exists without erasing it.
# Using "w" would overwrite and lose the first line — use "a" instead.

import tempfile

journal_path = tempfile.mktemp()
with open(journal_path, "w") as f:
    f.write("day 1: sunny\n")

# Append "day 2: rainy\n" to journal_path.
with open(journal_path, "w") as fh:   # TODO: change "w" to "a"
    fh.write("day 2: rainy\n")
