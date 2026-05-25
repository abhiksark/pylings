# Exercise: File IO 1
# I AM NOT DONE
#
# `data_path` is an absolute path to a new temp file.
# Write the string "hello, file!" to that file using open() and .write().
# The file should contain exactly that text after you are done.
#
# Hint: open(path, "w") returns a file object; call .write(text) on it,
# then .close() it — or use a with statement.

import tempfile

data_path = tempfile.mktemp()

# Write "hello, file!" to data_path.
f = open(data_path, "w")
f.write(???)
f.close()
