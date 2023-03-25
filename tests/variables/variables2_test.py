# Import the variables from the exercise file
import os
import sys

# Get the absolute path of the current module (the test file)
test_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the exercises directory relative to the test file
exercises_dir = os.path.join(test_dir, "..", "..")
# Add the exercises directory to the Python path
sys.path.append(exercises_dir)

from exercises.variables.variables2 import (
    a,
    b,
    c,
    diff_ab,
    product_ab,
    product_ac,
    quotient_ab,
    remainder_ab,
    sum_ab,
    sum_ac,
)


# Test code - do not modify
def test_variables2():
    # Test variable initialization
    assert isinstance(a, int), "a should be an integer"
    assert isinstance(b, int), "b should be an integer"
    assert isinstance(c, str), "c should be a string"

    # Test variable operations
    assert sum_ab == 13, "sum_ab should be 13"
    assert diff_ab == 7, "diff_ab should be 7"
    assert product_ab == 30, "product_ab should be 30"
    assert quotient_ab == 3.3333333333333335, "quotient_ab should be 3.3333333333333335"
    assert remainder_ab == 1, "remainder_ab should be 1"
    assert sum_ac == "10hello", "sum_ac should be '10hello'"
    assert product_ac == "hellohellohello", "product_ac should be 'hellohellohello'"
