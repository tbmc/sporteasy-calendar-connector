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

logger = logging.getLogger(__name__)

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
        logger.debug("Handling CORS preflight request")
        return flask.Response("", headers=CORS_HEADERS)
    return None


def _list_teams_response() -> str:
    username, password, _ = decode_data()
    logger.debug("Preparing list teams response for user=%s", username)
    connector = SporteasyConnector()
    connector.login(username, password)
    teams = connector.list_teams()
    logger.info("Listed %s teams for user=%s", len(teams), username)
    return json.dumps(teams)


def _generate_request_payload() -> str:
    input_data = cast(dict[str, str], flask.request.json)
    if not ({"username", "password", "team_id"} >= set(input_data.keys())):
        logger.warning(
            "Invalid keys in generate_request_payload: keys=%s",
            sorted(input_data.keys()),
        )
        raise Exception("Invalid keys")
    data = {
        "username": input_data["username"],
        "password": input_data["password"],
    }
    if input_data.get("team_id") is not None:
        data["team_id"] = input_data["team_id"]
    string = json.dumps(data)
    encrypted = encrypt_message(string)
    logger.info("Generated encrypted request payload (team_id_provided=%s)", "team_id" in data)
    return encrypted.decode("utf-8")


def _decode_encrypted_data() -> tuple[str, str, str | None]:
    data_encrypted = flask.request.args["data"]
    logger.debug("Decoding encrypted request payload")
    decrypted = decrypt_message(data_encrypted.encode("utf-8"))
    data = json.loads(decrypted)
    return data["username"], data["password"], data.get("team_id")


def request_handler() -> flask.Response:
    if flask.request.args.get("encrypted", "0") == "1":
        username, password, team_id = _decode_encrypted_data()
    else:
        username, password, team_id = decode_data()
    ip = flask.request.remote_addr
    logger.info("Incoming calendar request from ip=%s username=%s", ip, username)

    url_root = flask.request.url_root
    disable_save_login = flask.request.args.get("disable_save_login") is not None
    logger.debug(
        "Building calendar (save_login=%s, team_id=%s)",
        not disable_save_login,
        team_id,
    )
    calendar_converter = CalendarConverter()
    calendar_text = calendar_converter.get_calendar_text(
        username, password, not disable_save_login, url_root, team_id
    )

    logger.info("Calendar generated successfully for username=%s", username)

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
        presence_arg = flask.request.args["presence"].lower()
        presence: bool = presence_arg == PRESENCE.present
    except BadRequestKeyError:
        logger.warning("Missing parameter in presence change request")
        return flask.Response("Parameter missing", status=500)

    hash_token = generate_links_data(team_id, event_id, user_id, presence)
    if token != hash_token:
        logger.warning(
            "Invalid token for presence change (team_id=%s, event_id=%s, user_id=%s)",
            team_id,
            event_id,
            user_id,
        )
        raise BadTokenException()

    logger.info(
        "Updating presence (team_id=%s, event_id=%s, user_id=%s, presence=%s)",
        team_id,
        event_id,
        user_id,
        presence,
    )
    set_presence_to_event(int(team_id), int(event_id), int(user_id), presence)

    return flask.send_file("calendar_connector/html/auto_close.html")


@app.get("/api/list-teams")
def list_teams() -> flask.Response:
    try:
        return flask.Response(_list_teams_response(), headers=CORS_HEADERS)
    except Exception as e:
        logger.exception("Failed to list teams")
        return flask.Response(str(e), headers=CORS_HEADERS)


@app.post("/api/generate_request_payload")
def generate_request_payload() -> flask.Response:
    try:
        payload = _generate_request_payload()
        return flask.Response(payload, headers=CORS_HEADERS)
    except Exception as e:
        logger.exception("Failed to generate request payload")
        error = str(e)
        return flask.Response(error, headers=CORS_HEADERS)


@app.get("/api")
def main_request_api_handler() -> flask.Response:
    if os.environ.get("DEBUG"):
        logger.debug("DEBUG mode enabled; exceptions will not be caught")
        return request_handler()
    try:
        return request_handler()
    except Exception as e:
        logger.exception("Error while handling /api request")
        return flask.Response(str(e))


@app.get("/")
def serve_static_index() -> flask.Response:
    data = flask.request.args.get("data", None)
    if data is not None:
        # Redirect user to /api if data is passed to keep compatibility
        redirect_route = flask.url_for("main_request_api_handler")
        redirect_url = f"{redirect_route}?data={data}"
        logger.debug("Redirecting / with data query parameter to /api")
        return flask.redirect(redirect_url)  # type: ignore

    return send_from_directory("web-app/build", "index.html")


@app.get("/<path:path>")
def serve_static_files(path: str) -> flask.Response:
    return send_from_directory("web-app/build", path)


if __name__ == "__main__":
    logger.info("Starting Flask app")
    app.run(host="0.0.0.0")
