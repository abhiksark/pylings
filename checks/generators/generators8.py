assert list(Countdown(3)) == [3, 2, 1]
assert list(Countdown(1)) == [1]
assert list(Countdown(5)) == [5, 4, 3, 2, 1]
# Should be re-iterable: a fresh iteration each time.
cd = Countdown(3)
assert list(cd) == [3, 2, 1]
assert list(cd) == [3, 2, 1]
print("generators8 ✓")
