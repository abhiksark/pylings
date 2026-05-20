test_palindrome()
test_word_count()
test_title_case()
test_truncate()

import inspect

for fn, min_asserts in [
    (test_palindrome, 3),
    (test_word_count, 3),
    (test_title_case, 2),
    (test_truncate, 3),
]:
    src = inspect.getsource(fn)
    assert src.count("assert") >= min_asserts, (
        f"{fn.__name__} should contain at least {min_asserts} assertions"
    )

print("testing12 ✓")
