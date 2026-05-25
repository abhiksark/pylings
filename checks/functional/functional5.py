assert by_length == ["fig", "kiwi", "date", "apple", "banana"], (
    f"by_length should be ['fig', 'kiwi', 'date', 'apple', 'banana'], got {by_length}"
)
assert by_length[0] == "fig"
assert by_length[-1] == "banana"
print("functional5 ✓")
