assert validate_username("Alice") == "alice", f"expected 'alice', got {validate_username('Alice')!r}"
assert validate_username("User123") == "user123", f"expected 'user123', got {validate_username('User123')!r}"
assert validate_username("abc") == "abc", "3-char name should be valid"
assert validate_username("a" * 20) == "a" * 20, "20-char name should be valid"

# rule 1: type check
raised = False
try:
    validate_username(42)
except TypeError as e:
    raised = True
    assert "str" in str(e), f"TypeError message should mention 'str', got {e!r}"
assert raised, "validate_username(42) should raise TypeError"

# rule 2: too short
raised = False
try:
    validate_username("ab")
except ValueError as e:
    raised = True
assert raised, "validate_username('ab') should raise ValueError"

# rule 2: too long
raised = False
try:
    validate_username("a" * 21)
except ValueError:
    raised = True
assert raised, "a 21-char name should raise ValueError"

# rule 3: non-alphanumeric
raised = False
try:
    validate_username("bad name!")
except ValueError as e:
    raised = True
    assert "alphanumeric" in str(e), f"ValueError message should mention 'alphanumeric', got {e!r}"
assert raised, "validate_username('bad name!') should raise ValueError"
print("exceptions10 ✓")
