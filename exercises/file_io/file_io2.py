# Exercise: File IO 2
# I AM NOT DONE
#
# `note_path` points to a file that already contains the text "remember".
# Read the WHOLE file and store its text in the variable `contents`.
#
# Hint: open(path).read() returns the entire file as a string.

import tempfile

note_path = tempfile.mktemp()
with open(note_path, "w") as f:
    f.write("remember")

# Read the whole file into `contents`.
contents = ???
