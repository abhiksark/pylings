from pathlib import Path

assert processed == Path("data/raw.json")
assert parts[-2:] == ("data", "raw.json")
print("pathlib6 ok")
