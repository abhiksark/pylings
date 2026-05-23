# Exercise: Json 7
# I AM NOT DONE
#
# Goal: Decode settings, update one value, and encode them again.

import json

settings = json.loads('{"theme": "light", "font_size": 12}')
settings["theme"] = ???
encoded = json.dumps(settings, sort_keys=True)
