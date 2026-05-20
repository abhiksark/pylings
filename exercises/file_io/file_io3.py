# Exercise: File IO 3
# I AM NOT DONE
#
# Use a `with` statement to open `log_path` for writing ("w") and write
# the string "first entry" to it.  The `with` statement closes the file
# automatically when its block ends.
#
# Pattern:
#   with open(path, "w") as fh:
#       fh.write(text)

import tempfile

log_path = tempfile.mktemp()

# Replace the ??? so the with-block writes "first entry".
with open(log_path, "w") as fh:
    fh.write(???)
