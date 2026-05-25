# Exercise: Testing 6
# I AM NOT DONE
#
# Sometimes the correct behaviour is for a function to *raise* an exception.
# Test that with a try/except block:
#
#   try:
#       call_that_should_raise()
#       assert False, "expected an exception but none was raised"
#   except SomeError:
#       pass  # good — exception was raised as expected
#
# Complete `test_parse_positive` so it:
#   1. Asserts parse_positive("42") == 42  (happy path)
#   2. Verifies that parse_positive("-1") raises ValueError

def parse_positive(s):
    n = int(s)
    if n < 0:
        raise ValueError(f"{n} is not positive")
    return n


def test_parse_positive():
    # 1. assert the happy path
    # 2. use try/except to verify ValueError is raised for "-1"
    pass
