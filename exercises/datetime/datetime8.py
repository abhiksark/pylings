# Exercise: Datetime 8
# I AM NOT DONE
#
# Goal: Parse ISO date strings and find the earliest and latest dates.

from datetime import date

raw_dates = ["2026-05-23", "2024-01-01", "2025-12-31"]
parsed = [date.fromisoformat(value) for value in raw_dates]
earliest = ???
latest = ???
