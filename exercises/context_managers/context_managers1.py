# Exercise: Context Managers 1
# I AM NOT DONE
#
# Use a `with` statement to open `data_path` for writing and write the
# text "hello, context!" to it.  The with-block should handle opening
# and closing automatically — do NOT call .close() yourself.
#
# Hint: `with open(path, "w") as f:` opens the file; call `f.write(text)`
# inside the block.

import tempfile

data_path = tempfile.mktemp()

# Replace the bare open/write/close below with a with-statement.
f = open(data_path, "w")
f.write("hello, context!")
# Bug: .close() is missing — but the real fix is to use `with`.
