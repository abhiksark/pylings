# Exercise: Testing 5
# I AM NOT DONE
#
# Good tests exercise a function with several different inputs.
# Complete `test_clamp` to verify `clamp(value, lo, hi)` for each case:
#   clamp(5,  0, 10) == 5    (inside range)
#   clamp(-3, 0, 10) == 0    (below lo, should return lo)
#   clamp(15, 0, 10) == 10   (above hi, should return hi)
#   clamp(0,  0, 10) == 0    (at boundary lo)
#   clamp(10, 0, 10) == 10   (at boundary hi)

def clamp(value, lo, hi):
    return max(lo, min(value, hi))


def test_clamp():
    # write five assertions here
    pass
