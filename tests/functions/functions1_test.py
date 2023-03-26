import os
import sys

# Get the absolute path of the current module (the test file)
test_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the exercises directory relative to the test file
exercises_dir = os.path.join(test_dir, "..", "..")
# Add the exercises directory to the Python path
sys.path.append(exercises_dir)

# Import the function to be tested
from exercises.functions.functions1 import average


def test_average():
    # Test for positive numbers
    assert average(2, 4) == 3
    assert average(10, 20) == 15

    # Test for negative numbers
    assert average(-2, -4) == -3
    assert average(-10, -20) == -15

    # Test for fractions
    assert average(1.5, 2.5) == 2
    assert average(0.5, 1.5) == 1

    # Test for zero
    assert average(0, 0) == 0

    # Test for non-integer inputs
    assert average(3, 4.5) == 3.75
