assert can_read == True, f"can_read should be True, got {can_read!r}"
assert can_write == True, f"can_write should be True ('write' is a key), got {can_write!r}"
assert can_delete == False, f"can_delete should be False, got {can_delete!r}"
print("dictionaries8 ✓")
