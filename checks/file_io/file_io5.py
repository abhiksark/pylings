import os

with open(journal_path) as _f:
    _contents = _f.read()

assert _contents == "day 1: sunny\nday 2: rainy\n", (
    f"file should contain both lines, got {_contents!r}"
)

try:
    os.remove(journal_path)
except OSError:
    pass

print("file_io5 ✓")
