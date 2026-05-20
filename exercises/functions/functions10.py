# Exercise: Functions 10
# I AM NOT DONE
#
# Complete the helper function `is_palindrome` that takes a string and
# returns True if it reads the same forwards and backwards (ignoring
# case), and False otherwise.
# Example: is_palindrome("Racecar") -> True
# Example: is_palindrome("hello") -> False
#
# Then use it to build `palindromes`: a list of all strings from `words`
# that are palindromes.

words = ["racecar", "hello", "level", "world", "madam", "python", "noon"]

def is_palindrome(s):
    # Hint: compare s.lower() with its reverse (s.lower()[::-1])
    pass

palindromes = [w for w in words if is_palindrome(w)]
