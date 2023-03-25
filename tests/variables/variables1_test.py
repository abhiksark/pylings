# test_variable.py

import sys

import pytest

sys.append("../examples/variables")
from variables1 import a, b, c


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
