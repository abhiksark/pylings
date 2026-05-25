# Exercise: Json 8
# I AM NOT DONE
#
# Goal: Round-trip a nested object without losing values.

import json

original = {"project": "pylings", "tags": ["python", "practice"], "meta": {"level": 3}}
encoded = json.dumps(original, sort_keys=True)
decoded = ???
tag_count = len(decoded["tags"])
level = decoded["meta"]["level"]
