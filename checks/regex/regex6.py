assert is_valid is True, "ABCDE123 should be valid"
assert not bool(re.fullmatch(pattern, "ABCDE12")), "ABCDE12 (2 digits) should be invalid"
assert not bool(re.fullmatch(pattern, "abcde123")), "abcde123 (lowercase) should be invalid"
assert not bool(re.fullmatch(pattern, "ABCDE1234")), "ABCDE1234 (4 digits) should be invalid"
assert not bool(re.fullmatch(pattern, "ABCD123")), "ABCD123 (4 letters) should be invalid"
print("regex6 ✓")
