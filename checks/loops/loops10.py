assert len(summary) == 4, f"Expected 4 entries (skipping the zero-amount one), got {len(summary)}"
assert summary[0] == {"index": 1, "amount": 100, "balance": 100}, f"First entry wrong: {summary[0]}"
assert summary[1] == {"index": 3, "amount": 40, "balance": 60}, f"Second entry wrong: {summary[1]}"
assert summary[2] == {"index": 4, "amount": 200, "balance": 260}, f"Third entry wrong: {summary[2]}"
assert summary[3] == {"index": 5, "amount": 60, "balance": 200}, f"Fourth entry wrong: {summary[3]}"
print("loops10 ✓")
