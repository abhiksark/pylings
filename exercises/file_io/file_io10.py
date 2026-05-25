# Exercise: File IO 10
# I AM NOT DONE
#
# `src_path` contains three lines of mixed-case text.
# Copy the file to `dst_path`, converting every line to UPPERCASE.
# After your code runs, `dst_path` should contain the uppercased text.
#
# Steps:
#   1. Open src_path for reading.
#   2. Open dst_path for writing.
#   3. For each line read from src, write line.upper() to dst.

import tempfile

src_path = tempfile.mktemp()
dst_path = tempfile.mktemp()

with open(src_path, "w") as f:
    f.write("hello world\npython is fun\nfile io rocks\n")

# Copy src_path to dst_path, converting each line to uppercase.
with open(src_path) as src:
    with open(dst_path, "w") as dst:
        for line in src:
            dst.write(line)   # TODO: write line.upper() instead of line
