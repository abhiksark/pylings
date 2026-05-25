import os

with open(log_path) as _f:
    _contents = _f.read()

assert _contents == "first entry", (
    f"file should contain 'first entry', got {_contents!r}"
)

try:
    os.remove(log_path)
except OSError:
    pass

print("file_io3 ✓")
