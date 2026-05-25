import os

assert word_count == 9, f"expected 9 words, got {word_count!r}"

try:
    os.remove(essay_path)
except OSError:
    pass

print("file_io9 ✓")
