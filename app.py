import os

import json
import logging
from typing import cast

import flask
from flask import send_from_directory
from werkzeug.exceptions import BadRequestKeyError

from calendar_connector.calendar_converter import CalendarConverter
from calendar_connector.consts import route_change_presence, PRESENCE
from calendar_connector.data_decoder import decode_data
from calendar_connector.sporteasy_connector import SporteasyConnector
from calendar_connector.database.user import generate_links_data
from calendar_connector.custom_exceptions import BadTokenException
from calendar_connector.presence_updater import set_presence_to_event
from calendar_connector.database.create_tables import create_db
from calendar_connector.cryptography import encrypt_message, decrypt_message

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

create_db()

app = flask.Flask(__name__)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Headers": "*",
}


@app.before_request
def handle_preflight() -> flask.Response | None:
    if flask.request.method == "OPTIONS":
        return flask.Response("", headers=CORS_HEADERS)
    return None


def _list_teams_response() -> str:
    username, password, _ = decode_data()
    connector = SporteasyConnector()
    connector.login(username, password)
    teams = connector.list_teams()
    return json.dumps(teams)


def _generate_request_payload() -> str:
    input_data = cast(dict[str, str], flask.request.json)
    if not ({"username", "password", "team_id"} >= set(input_data.keys())):
        raise Exception("Invalid keys")
    data = {
        "username": input_data["username"],
        "password": input_data["password"],
    }
    if input_data.get("team_id") is not None:
        data["team_id"] = input_data["team_id"]
    string = json.dumps(data)
    encrypted = encrypt_message(string)
    return encrypted.decode("utf-8")


def _decode_encrypted_data() -> tuple[str, str, str | None]:
    data_encrypted = flask.request.args["data"]
    decrypted = decrypt_message(data_encrypted.encode("utf-8"))
    data = json.loads(decrypted)
    return data["username"], data["password"], data.get("team_id")


def request_handler() -> flask.Response:
    if flask.request.args.get("encrypted", "0") == "1":
        username, password, team_id = _decode_encrypted_data()
    else:
        username, password, team_id = decode_data()
    ip = flask.request.remote_addr
    logging.info(f"New incoming request from {ip=} and {username=}")

    url_root = flask.request.url_root
    disable_save_login = flask.request.args.get("disable_save_login") is not None
    calendar_converter = CalendarConverter()
    calendar_text = calendar_converter.get_calendar_text(
        username, password, not disable_save_login, url_root, team_id
    )

    return flask.Response(
        calendar_text,
        headers={"Content-Type": "text/calendar; charset=utf-8"},
        mimetype="text/calendar",
    )


@app.route(route_change_presence)
def change_my_presence() -> flask.Response:
    try:
        team_id = flask.request.args["team_id"]
        event_id = flask.request.args["event_id"]
        user_id = flask.request.args["user_id"]
        token = flask.request.args["token"]
        presence = flask.request.args["presence"].lower() == PRESENCE.present
    except BadRequestKeyError as e:
        return flask.Response("Parameter missing", status=500)

    hash_token = generate_links_data(team_id, event_id, user_id, presence)
    if token != hash_token:
        raise BadTokenException()

    set_presence_to_event(int(team_id), int(event_id), int(user_id), presence)

    return flask.send_file("calendar_connector/html/auto_close.html")


@app.get("/api/list-teams")
def list_teams() -> flask.Response:
    try:
        return flask.Response(_list_teams_response(), headers=CORS_HEADERS)
    except Exception as e:
        return flask.Response(str(e), headers=CORS_HEADERS)


@app.post("/api/generate_request_payload")
def generate_request_payload() -> flask.Response:
    try:
        payload = _generate_request_payload()
        return flask.Response(payload, headers=CORS_HEADERS)
    except Exception as e:
        error = str(e)
        return flask.Response(error, headers=CORS_HEADERS)


@app.get("/api")
def main_request_api_handler() -> flask.Response:
    if os.environ.get("DEBUG"):
        return request_handler()
    try:
        return request_handler()
    except Exception as e:
        return flask.Response(str(e))


@app.get("/")
def serve_static_index() -> flask.Response:
    data = flask.request.args.get("data", None)
    if data is not None:
        # Redirect user to /api if data is passed to keep compatibility
        redirect_route = flask.url_for("main_request_api_handler")
        redirect_url = f"{redirect_route}?data={data}"
        return flask.redirect(redirect_url)  # type: ignore

    return send_from_directory("web-app/build", "index.html")


@app.get("/<path:path>")
def serve_static_files(path: str) -> flask.Response:
    return send_from_directory("web-app/build", path)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
