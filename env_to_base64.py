import json
import base64
import urllib.parse
from dotenv import dotenv_values

env = dotenv_values(".env")

username = env["username"]
password = env["password"]

# Team is optional
team_id: str | None = env.get("team_id")

data = {
    "username": username,
    "password": password,
}

if team_id is not None:
    data["team_id"] = team_id

data_str = json.dumps(data)
data_64 = base64.b64encode(data_str.encode("utf-8"))

data_b64 = data_64.decode("utf-8")

encoded_data = urllib.parse.urlencode({
    "data": data_b64
})

print(f'Data: "{encoded_data}"\n')
print("Default URL:")
print(f"https://sporteasy-calendar-connector.tbmc.ovh?" + encoded_data)
