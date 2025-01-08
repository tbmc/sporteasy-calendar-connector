import json
import base64
from unittest import mock

from calendar_connector.data_decoder import decode_data


class __UtilArgsData:
    args: dict[str, str]

    def __init__(self) -> None:
        self.args = {}


def test_decode_data_flask_data() -> None:
    data = base64.b64encode(
        json.dumps(
            {
                "username": "flask_username",
                "password": "flask_password",
                "team_id": "flask_team_id",
            }
        ).encode("utf-8")
    ).decode("utf-8")

    util_args = __UtilArgsData()
    util_args.args = {"data": data}

    with mock.patch("flask.request", util_args):
        username, password, team_id = decode_data()

    assert username == "flask_username"
    assert password == "flask_password"
    assert team_id == "flask_team_id"


def test_decode_data_flask_args() -> None:
    util_args = __UtilArgsData()
    util_args.args = {
        "username": "flask_args_username",
        "password": "flask_args_password",
        "team_id": "flask_args_team_id",
    }

    with mock.patch("flask.request", util_args):
        username, password, team_id = decode_data()

    assert username == "flask_args_username"
    assert password == "flask_args_password"
    assert team_id == "flask_args_team_id"


def test_decode_data_env() -> None:
    util_args = __UtilArgsData()
    env = {
        "username": "env_username",
        "password": "env_password",
        "team_id": "env_team_id",
    }
    with (
        mock.patch("flask.request", util_args),
        mock.patch("calendar_connector.data_decoder._env", env),
    ):
        username, password, team_id = decode_data()

    assert username == "env_username"
    assert password == "env_password"
    assert team_id == "env_team_id"
