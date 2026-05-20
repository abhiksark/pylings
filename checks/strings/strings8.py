assert message == "Hello, Grace! You are 30 years old.", f"message should be 'Hello, Grace! You are 30 years old.', got {message!r}"
assert message.startswith("f") is False, "Use an f-string (f'...'), not concatenation"
print("strings8 ✓")
