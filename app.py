import os
import base64
import json
import logging

import flask
from calendar_converter import CalendarConverter
from dotenv import dotenv_values

logging.basicConfig(filename="access.log", filemode="a", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

app = flask.Flask(__name__)

env = dotenv_values(".env")


def request_handler() -> flask.Response:
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

    ip = flask.request.remote_addr
    logging.info(f"New incoming request from {ip=} and {username=}")

    calendar_converter = CalendarConverter()
    calendar_text = calendar_converter.get_calendar_text(username, password, team_id)

    return flask.Response(
        calendar_text,
        headers={
            "Content-Type": "text/calendar; charset=utf-8"
        },
        mimetype="text/calendar",
    )


@app.route("/")
def main_request_handler() -> flask.Response:
    if os.environ.get("DEBUG"):
        return request_handler()

    try:
        return request_handler()
    except Exception as e:
        return flask.Response(str(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
