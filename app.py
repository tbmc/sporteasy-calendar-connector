import os
import base64
import json
import logging

import flask
from calendar_converter import CalendarConverter
from dotenv import dotenv_values

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

app = flask.Flask(__name__)

env = dotenv_values(".env")

with open("index.html", encoding="utf-8") as f:
    html_content = f.read()


def _decode_data() -> tuple[str, str, str | None]:
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


def _request_handler_with_data() -> flask.Response:
    username, password, team_id = _decode_data()
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


def _list_teams_response() -> str:
    username, password, _ = _decode_data()
    calendar_converter = CalendarConverter()
    calendar_converter.login(username, password)
    teams = calendar_converter.list_teams()
    return json.dumps(teams)


def request_handler() -> flask.Response:
    # If no data, return html page
    if "data" not in flask.request.args:
        return flask.Response(html_content)
    return _request_handler_with_data()


@app.route("/list-teams")
def list_teams() -> flask.Response:
    try:
        return flask.Response(_list_teams_response())
    except Exception as e:
        return flask.Response(e)


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
