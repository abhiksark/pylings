import os

assert isinstance(lines, list), f"lines should be a list, got {type(lines).__name__}"
assert len(lines) == 3, f"expected 3 lines, got {len(lines)}"
assert lines[0] == "roses are red\n", f"first line wrong: {lines[0]!r}"
assert lines[1] == "violets are blue\n", f"second line wrong: {lines[1]!r}"
assert lines[2] == "python is great\n", f"third line wrong: {lines[2]!r}"

try:
    os.remove(poem_path)
except OSError:
    pass

print("file_io4 ✓")
