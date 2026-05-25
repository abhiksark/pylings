import os

with open(data_path) as _f:
    _contents = _f.read()

assert _contents == "hello, file!", (
    f"file should contain 'hello, file!', got {_contents!r}"
)

try:
    os.remove(data_path)
except OSError:
    pass

print("file_io1 ✓")
