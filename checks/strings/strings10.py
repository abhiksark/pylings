assert report == "Item: widget | Qty: 42 | Price: $3.99", (
    f"report should be 'Item: widget | Qty: 42 | Price: $3.99', got {report!r}"
)
assert isinstance(report, str), "report should be a string"
print("strings10 ✓")
