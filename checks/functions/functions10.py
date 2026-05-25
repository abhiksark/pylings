assert callable(is_palindrome), "is_palindrome should be a function"
assert is_palindrome("racecar") is True
assert is_palindrome("Racecar") is True
assert is_palindrome("hello") is False
assert is_palindrome("level") is True
assert is_palindrome("madam") is True
assert is_palindrome("noon") is True
assert is_palindrome("python") is False
assert palindromes == ["racecar", "level", "madam", "noon"], (
    f"Expected ['racecar', 'level', 'madam', 'noon'], got {palindromes!r}"
)
print("functions10 ✓")
