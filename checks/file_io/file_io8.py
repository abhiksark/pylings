import os

assert result == "Hello, World!", (
    f"result should be 'Hello, World!', got {result!r}"
)

try:
    os.remove(source_path)
except OSError:
    pass

print("file_io8 ✓")
