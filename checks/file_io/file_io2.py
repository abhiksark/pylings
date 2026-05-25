import os

assert contents == "remember", f"contents should be the file's text, got {contents!r}"

try:
    os.remove(note_path)
except OSError:
    pass

print("file_io2 ✓")
