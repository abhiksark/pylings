assert result is not None, "result should be a match object, not None"
assert result.group() == "hello", "matched text should be 'hello'"
print("regex1 ✓")
