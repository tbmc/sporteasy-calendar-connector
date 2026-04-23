import base64
import flask
import json
import logging

from .env import _env

logger = logging.getLogger(__name__)


def decode_data() -> tuple[str, str, str | None]:
    username: str | None = None
    password: str | None = None
    team_id: str | None = None

    data_b64 = flask.request.args.get("data")
    if data_b64 is not None:
        logger.debug("Decoding credentials from base64 query parameter")
        decoded = base64.b64decode(data_b64.encode("utf-8"))
        data = json.loads(decoded)
        username = data["username"]
        password = data["password"]
        team_id = data.get("team_id")

    if username is None or password is None:
        logger.debug("Reading credentials from query parameters")
        username = flask.request.args.get("username")
        password = flask.request.args.get("password")
        team_id = flask.request.args.get("team_id")

    if username is None or password is None:
        logger.debug("Reading credentials from .env fallback")
        username = _env.get("username")
        password = _env.get("password")
        team_id = _env.get("team_id")
    if username is None or not any(username) or password is None or not any(password):
        logger.warning(
            "Missing username/password after all credential sources were checked"
        )
        raise Exception("Missing username and password")

    logger.debug(
        "Credentials successfully decoded (team_id_provided=%s)", team_id is not None
    )

    return username, password, team_id
