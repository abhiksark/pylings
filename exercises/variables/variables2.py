# Exercise: Variables 2
# ----------------------


# not done

# Define the variables a, b, and c below
a = 10
b = 3
c = "hello"

# Perform some operations on the variables
sum_ab = a + b
diff_ab = a - b
product_ab = a * b
quotient_ab = a / b
remainder_ab = a % b
sum_ac = str(a) + c
product_ac = c * b

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
