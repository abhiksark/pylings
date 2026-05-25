assert result is not None, "result should be a match object, not None"
assert result.group() == "python", "matched text should be 'python'"
print("regex2 ✓")
