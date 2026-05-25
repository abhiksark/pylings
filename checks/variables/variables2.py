sum_ab = a + b
diff_ab = a - b
product_ab = a * b
quotient_ab = a / b
remainder_ab = a % b
sum_ac = str(a) + c
product_ac = c * b

assert isinstance(a, int), "a should be an integer"
assert isinstance(b, int), "b should be an integer"
assert isinstance(c, str), "c should be a string"
assert sum_ab == 13, "sum_ab should be 13"
assert diff_ab == 7, "diff_ab should be 7"
assert product_ab == 30, "product_ab should be 30"
assert quotient_ab == 3.3333333333333335
assert remainder_ab == 1
assert sum_ac == "10hello"
assert product_ac == "hellohellohello"
print("variables2 ✓")
