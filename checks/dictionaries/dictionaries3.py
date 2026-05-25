assert scores.get("diana") == 91, f"scores['diana'] should be 91, got {scores.get('diana')!r}"
assert scores["alice"] == 88, f"scores['alice'] should be 88 after update, got {scores['alice']!r}"
assert scores["bob"] == 60, "scores['bob'] should remain 60"
assert scores["carol"] == 82, "scores['carol'] should remain 82"
print("dictionaries3 ✓")
