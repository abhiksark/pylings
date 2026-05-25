assert isinstance(word_index, dict), "word_index should be a dict"
assert word_index == {"apple": 0, "banana": 1, "cherry": 2, "date": 3}, (
    f"unexpected word_index: {word_index!r}"
)
print("comprehensions10 ✓")
