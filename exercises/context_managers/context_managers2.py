# Exercise: Context Managers 2
# I AM NOT DONE
#
# After the with-block finishes, the file object should be closed
# automatically.  The code below opens a file WITHOUT a with-statement,
# so `f.closed` is False after the write.
#
# Fix it: replace the bare open/write/close sequence with a with-statement
# that opens `data_path` for writing and writes "closed check".
# After the with-block, `f` must be the file object and `f.closed` must be True.

import tempfile

data_path = tempfile.mktemp()

# Bug: no with-statement — the file stays open until garbage-collected.
f = open(data_path, "w")
f.write("closed check")
# .close() is intentionally omitted to illustrate the problem.
