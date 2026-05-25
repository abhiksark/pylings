assert first_ten == list(range(1, 11)), (
    f"expected [1..10], got {first_ten}"
)
# Confirm the generator really is infinite: pull 1000 values.
big = list(itertools.islice(natural_numbers(), 1000))
assert len(big) == 1000
assert big[-1] == 1000
print("generators6 ✓")
