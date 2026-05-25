assert list(running_total([1, 2, 3, 4])) == [1, 3, 6, 10]
assert list(running_total([10, -3, 7])) == [10, 7, 14]
assert list(running_total([])) == []
assert list(running_total([5])) == [5]
# Works as a streaming pipeline over a generator input.
assert list(running_total(x * x for x in range(1, 5))) == [1, 5, 14, 30]
print("generators10 ✓")
