import json
import base64
import urllib.parse
from dotenv import dotenv_values

env = dotenv_values(".env")

username = env["username"]
password = env["password"]

data = {
    "username": username,
    "password": password,
}

params = urllib.parse.urlencode(data)

data_str = json.dumps(data)
data_64 = base64.b64encode(data_str.encode("utf-8"))

data_b64 = data_64.decode("utf-8")

print(f"https://sporteasy-converter.***REMOVED***?" + urllib.parse.urlencode({
    "data": data_b64
}))
