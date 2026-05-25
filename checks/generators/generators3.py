assert collected == [2, 4, 6, 8], f"expected [2, 4, 6, 8], got {collected}"
assert list(evens_up_to(5)) == [2, 4]
assert list(evens_up_to(1)) == []
print("generators3 ✓")
