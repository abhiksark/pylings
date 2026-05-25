import random as _random
import math as _math
import statistics as _statistics

_random.seed(0)
_expected_data = [_random.randint(1, 100) for _ in range(10)]
_expected_mean = _statistics.mean(_expected_data)
_expected_max_sqrt = _math.sqrt(max(_expected_data))

assert data == _expected_data, f"data should be {_expected_data}"
assert data_mean == _expected_mean, f"data_mean should be {_expected_mean}"
assert abs(data_max_sqrt - _expected_max_sqrt) < 1e-9, (
    f"data_max_sqrt should be {_expected_max_sqrt}"
)
print("modules8 ✓")
