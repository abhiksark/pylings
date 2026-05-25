assert ml.items == [1, 2], f"items should be [1, 2], got {ml.items}"
assert ml.log == ["done"], f"log should be ['done'] after exit, got {ml.log}"
print("context_managers4 ✓")
