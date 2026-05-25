# Exercise: File IO 9
# I AM NOT DONE
#
# `essay_path` contains a short text with multiple words.
# Count the total number of words in the file and store the count in
# the variable `word_count`.
#
# A word is any whitespace-separated token — str.split() with no
# argument splits on any whitespace and discards empty strings.

import tempfile

essay_path = tempfile.mktemp()
with open(essay_path, "w") as f:
    f.write("the quick brown fox jumps over the lazy dog")

# Count the words in essay_path and store in `word_count`.
with open(essay_path) as fh:
    word_count = len(fh.read())   # TODO: split into words before taking len()
