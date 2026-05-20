# Exercise: Testing 12
# I AM NOT DONE
#
# A test suite is a collection of test functions that together give
# confidence in a whole module. Write a *separate* test function for each
# concern rather than cramming everything into one.
#
# Below is a small "string_utils" module. Write four test functions:
#
#   test_palindrome()    — verify is_palindrome for at least 3 inputs
#                          (one true, one false, one edge case like "")
#   test_word_count()    — verify word_count for at least 3 inputs
#                          (normal sentence, single word, empty string)
#   test_title_case()    — verify to_title_case for at least 2 inputs
#   test_truncate()      — verify truncate for at least 3 inputs
#                          (short string unchanged, long string truncated,
#                           boundary length exactly)

def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]


def word_count(s):
    if not s.strip():
        return 0
    return len(s.split())


def to_title_case(s):
    return s.title()


def truncate(s, max_len):
    return s if len(s) <= max_len else s[:max_len] + "..."


def test_palindrome():
    pass


def test_word_count():
    pass


def test_title_case():
    pass


def test_truncate():
    pass
