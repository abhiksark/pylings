# Exercise: Json 4
# I AM NOT DONE
#
# Goal: Use json.dump and json.load with a StringIO buffer.

import io
import json

payload = {"ok": True, "count": 3}
buffer = io.StringIO()
json.dump(???, buffer)
buffer.seek(0)
restored = json.load(buffer)
