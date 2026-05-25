assert gravity.value == 9.8
assert gravity.unit == "m/s²", f"got {gravity.unit!r}"
assert named.unit == "km/h"
print("dataclasses3 ✓")
