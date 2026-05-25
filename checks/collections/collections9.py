assert combined["apple"] == 7, "5 + 2 = 7 apples"
assert combined["banana"] == 7, "3 + 4 = 7 bananas"
assert combined["cherry"] == 2, "2 + 0 = 2 cherries"
assert combined["date"] == 1, "0 + 1 = 1 date"
assert remainder["apple"] == 3, "7 - 4 = 3 apples remain"
assert remainder["banana"] == 2, "7 - 5 = 2 bananas remain"
assert remainder["cherry"] == 1, "2 - 1 = 1 cherry remains"
assert "date" not in remainder or remainder["date"] == 1, "date was not sold"
print("collections9 ✓")
