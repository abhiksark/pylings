# Exercise: File IO 7
# I AM NOT DONE
#
# You have a list of strings called `words`.
# Write them to `words_path` so that each word appears on its own line.
# The file should contain exactly:
#   "alpha\nbeta\ngamma\n"
#
# Hint: fh.writelines(iterable) writes each item without adding newlines,
# so you need to ensure each string ends with "\n" before passing them in.
# Alternatively, use a loop: for w in words: fh.write(w + "\n")

import tempfile

words_path = tempfile.mktemp()
words = ["alpha", "beta", "gamma"]

# Write each word to words_path on its own line.
with open(words_path, "w") as fh:
    fh.writelines(words)   # TODO: each word needs a newline at the end
