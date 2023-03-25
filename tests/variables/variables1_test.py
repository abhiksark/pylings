# test_variable.py

import os
import sys

# Get the absolute path of the current module (the test file)
test_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the exercises directory relative to the test file
exercises_dir = os.path.join(test_dir, "..", "..")
# Add the exercises directory to the Python path
sys.path.append(exercises_dir)

from exercises.variables.variables1 import a, b, c


def test_a_is_int():
    assert isinstance(a, int)


def test_b_is_float():
    assert isinstance(b, float)


def test_c_is_str():
    assert isinstance(c, str)


def test_a_default_value():
    assert a == 0


def test_b_default_value():
    assert b == 0.0


def test_c_default_value():
    assert c == ""
