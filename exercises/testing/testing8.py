# Exercise: Testing 8
# I AM NOT DONE
#
# pytest's @pytest.mark.parametrize runs the same test for many inputs.
# Without pytest's collector you can get the same benefit by looping:
#
#   def test_something():
#       cases = [(input1, expected1), (input2, expected2), ...]
#       for inp, expected in cases:
#           assert fn(inp) == expected, f"fn({inp!r}) expected {expected!r}"
#
# Complete `test_fahrenheit_to_celsius` by filling in the `cases` list with
# at least these four (fahrenheit, celsius) pairs:
#   (32,  0.0)
#   (212, 100.0)
#   (98.6, 37.0)
#   (-40, -40.0)
# The loop body is already written — only `cases` needs to be filled in.

def fahrenheit_to_celsius(f):
    return round((f - 32) * 5 / 9, 10)


def test_fahrenheit_to_celsius():
    cases = []  # replace with a list of (fahrenheit, celsius) tuples
    for f, expected in cases:
        assert abs(fahrenheit_to_celsius(f) - expected) < 1e-6, (
            f"fahrenheit_to_celsius({f}) expected {expected}"
        )
