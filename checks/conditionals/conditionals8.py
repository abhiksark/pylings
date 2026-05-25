assert describe(0) == "empty", "0 is falsy"
assert describe("") == "empty", "empty string is falsy"
assert describe([]) == "empty", "empty list is falsy"
assert describe(None) == "empty", "None is falsy"
assert describe(1) == "has content", "1 is truthy"
assert describe("hello") == "has content", "non-empty string is truthy"
assert describe([1, 2]) == "has content", "non-empty list is truthy"
assert describe(0.1) == "has content", "non-zero float is truthy"
print("conditionals8 ✓")
