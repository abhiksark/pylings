# Exercise: File IO 8
# I AM NOT DONE
#
# `source_path` contains the text "  Hello, World!  " (with surrounding spaces).
# Read the file, strip the leading/trailing whitespace from the content,
# and store the cleaned text in `result`.
#
# Hint: str.strip() removes surrounding whitespace from a string.

import tempfile

source_path = tempfile.mktemp()
with open(source_path, "w") as f:
    f.write("  Hello, World!  ")

# Read the file and strip whitespace; store in `result`.
with open(source_path) as fh:
    result = fh.read()   # TODO: call .strip() on the result
