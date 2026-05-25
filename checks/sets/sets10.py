assert isinstance(attended_both, set), "attended_both should be a set"
assert attended_both == {"bob", "carol"}, f"attended_both should be {{'bob', 'carol'}}, got {attended_both!r}"

assert isinstance(attended_any, set), "attended_any should be a set"
assert attended_any == {"alice", "bob", "carol", "dave", "eve", "frank"}, (
    f"attended_any wrong, got {attended_any!r}"
)

assert isinstance(only_day1, set), "only_day1 should be a set"
assert only_day1 == {"alice", "dave"}, f"only_day1 should be {{'alice', 'dave'}}, got {only_day1!r}"

assert isinstance(only_day2, set), "only_day2 should be a set"
assert only_day2 == {"eve", "frank"}, f"only_day2 should be {{'eve', 'frank'}}, got {only_day2!r}"

print("sets10 ✓")
