import random as _random

_random.seed(42)
_expected = _random.randint(1, 10)

assert isinstance(pick, int), "pick should be an int"
assert pick == _expected, f"pick should be {_expected} when seeded with 42"
print("modules4 ✓")
