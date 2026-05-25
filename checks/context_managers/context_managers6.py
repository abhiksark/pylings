assert counter == [1, 2, "finished"], (
    f"counter should be [1, 2, 'finished'] after the with-block, got {counter!r}"
)
print("context_managers6 ✓")
