# Exercise: Json 6
# I AM NOT DONE
#
# Goal: Parse a JSON array and collect the active user names.

import json

raw = '[{"name": "Ada", "active": true}, {"name": "Lin", "active": false}, {"name": "Guido", "active": true}]'
users = json.loads(raw)
active_names = ???
