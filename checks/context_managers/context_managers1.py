import os

with open(data_path) as _f:
    _contents = _f.read()

assert _contents == "hello, context!", (
    f"file should contain 'hello, context!', got {_contents!r}"
)

try:
    os.remove(data_path)
except OSError:
    pass

print("context_managers1 ✓")
