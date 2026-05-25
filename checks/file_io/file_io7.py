import os

with open(words_path) as _f:
    _contents = _f.read()

assert _contents == "alpha\nbeta\ngamma\n", (
    f"file should contain each word on its own line, got {_contents!r}"
)

try:
    os.remove(words_path)
except OSError:
    pass

print("file_io7 ✓")
