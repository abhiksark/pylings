assert describe_error("3.14") == 3.14, f"expected 3.14, got {describe_error('3.14')!r}"
assert describe_error("10") == 10.0, f"expected 10.0, got {describe_error('10')!r}"

result = describe_error("hello")
assert isinstance(result, str), "on bad input, describe_error should return a str"
assert len(result) > 0, "the returned error string should not be empty"
assert "hello" in result, f"expected the bad value to appear in the message, got {result!r}"
print("exceptions3 ✓")
