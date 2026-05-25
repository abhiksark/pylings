assert is_closed(True) == False, "open shop is not closed"
assert is_closed(False) == True, "closed shop is closed"
assert neither_zero(3, 5) == True, "3 and 5 are both non-zero"
assert neither_zero(0, 5) == False, "a is zero"
assert neither_zero(3, 0) == False, "b is zero"
assert neither_zero(0, 0) == False, "both are zero"
print("conditionals6 ✓")
