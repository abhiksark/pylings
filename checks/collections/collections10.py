assert grouped["api"] == [120, 95, 110, 85, 100], "api response times"
assert grouped["web"] == [45, 60, 55, 50], "web response times"
assert grouped["db"] == [300, 280, 310], "db response times"

assert hit_counts["api"] == 5, "api was hit 5 times"
assert hit_counts["web"] == 4, "web was hit 4 times"
assert hit_counts["db"] == 3, "db was hit 3 times"

assert top_category == "api", "api has the most requests"

assert abs(avg_times["api"] - 102.0) < 1e-9, "api avg is 510/5 = 102.0"
assert abs(avg_times["web"] - 52.5) < 1e-9, "web avg is 210/4 = 52.5"
assert abs(avg_times["db"] - 296.666_666_7) < 1e-4, "db avg is 890/3"

print("collections10 ✓")
