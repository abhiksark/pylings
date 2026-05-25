# Exercise: Testing 7
# I AM NOT DONE
#
# Beyond checking that an exception is raised, you often need to verify
# its *message*. Capture the exception with `as e` and inspect `str(e)`:
#
#   try:
#       risky()
#       assert False, "expected ValueError"
#   except ValueError as e:
#       assert "some text" in str(e), f"unexpected message: {e}"
#
# Complete `test_divide_message` so it:
#   1. Asserts divide(10, 2) == 5.0
#   2. Catches the ValueError raised by divide(5, 0) and asserts
#      the message contains "zero"

def divide(a, b):
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b


def test_divide_message():
    # 1. happy-path assertion
    # 2. catch ValueError and check its message contains "zero"
    pass
