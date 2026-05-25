import os

assert total == 150, f"expected total == 150, got {total!r}"

try:
    os.remove(numbers_path)
except OSError:
    pass

print("file_io6 ✓")
