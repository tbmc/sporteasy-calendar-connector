import os

import json
import logging

import flask
from flask import send_from_directory
from calendar_connector.calendar_converter import CalendarConverter
from calendar_connector.data_decoder import decode_data

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

app = flask.Flask(__name__)

CORS_HEADERS = {"Access-Control-Allow-Origin": "*"}


def _list_teams_response() -> str:
    username, password, _ = decode_data()
    calendar_converter = CalendarConverter()
    calendar_converter.login(username, password)
    teams = calendar_converter.list_teams()
    return json.dumps(teams)


def request_handler() -> flask.Response:
    username, password, team_id = decode_data()
    ip = flask.request.remote_addr
    logging.info(f"New incoming request from {ip=} and {username=}")

    calendar_converter = CalendarConverter()
    calendar_text = calendar_converter.get_calendar_text(username, password, team_id)

    return flask.Response(
        calendar_text,
        headers={"Content-Type": "text/calendar; charset=utf-8"},
        mimetype="text/calendar",
    )


@app.route("/api/list-teams")
def list_teams() -> flask.Response:
    if flask.request.method == "OPTIONS":
        return flask.Response("", headers=CORS_HEADERS)
    try:
        return flask.Response(_list_teams_response(), headers=CORS_HEADERS)
    except Exception as e:
        return flask.Response(str(e), headers=CORS_HEADERS)


@app.route("/api")
def main_request_api_handler() -> flask.Response:
    if os.environ.get("DEBUG"):
        return request_handler()
    try:
        return request_handler()
    except Exception as e:
        return flask.Response(str(e))


@app.route("/")
def serve_static_index() -> flask.Response:
    data = flask.request.args.get("data", None)
    if data is not None:
        # Redirect user to /api if data is passed to keep compatibility
        redirect_route = flask.url_for("main_request_api_handler")
        redirect_url = f"{redirect_route}?data={data}"
        return flask.redirect(redirect_url)

    return send_from_directory("web-app/build", "index.html")


@app.route("/<path:path>")
def serve_static_files(path: str) -> flask.Response:
    return send_from_directory("web-app/build", path)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
