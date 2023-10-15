import base64
import flask
import json

from .env import env


def decode_data() -> tuple[str, str, str | None]:
    username: str | None = None
    password: str | None = None
    team_id: str | None = None

    data_b64 = flask.request.args.get("data")
    if data_b64 is not None:
        decoded = base64.b64decode(data_b64.encode("utf-8"))
        data = json.loads(decoded)
        username = data["username"]
        password = data["password"]
        team_id = data.get("team_id")

    if username is None or password is None:
        username = flask.request.args.get("username")
        password = flask.request.args.get("password")
        team_id = flask.request.args.get("team_id")

    if username is None or password is None:
        username = env.get("username")
        password = env.get("password")
        team_id = env.get("team_id")
    if username is None or not any(username) or password is None or not any(password):
        raise Exception("Missing username and password")

    return username, password, team_id
