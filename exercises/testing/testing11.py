# Exercise: Testing 11
# I AM NOT DONE
#
# Testing a class means: construct an instance, call its methods, and
# assert the resulting state is correct.
#
# Complete `test_counter` to verify the Counter class:
#   1. A new Counter starts at 0.
#   2. After calling increment() once, value is 1.
#   3. After calling increment() again, value is 2.
#   4. After calling reset(), value is back to 0.

class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def reset(self):
        self.value = 0


def test_counter():
    # 1. create a Counter instance
    # 2-4. assert state after each method call
    pass
