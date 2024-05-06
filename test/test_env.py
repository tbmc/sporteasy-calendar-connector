from unittest import mock

from utils.env import load_env_data


def test_env() -> None:
    env = {
        "username": "u",
        "password": "p",
        "team_id": "ti",
    }

    with mock.patch("utils.env.env", env):
        username, password, team_id = load_env_data()

    assert username == "u"
    assert password == "p"
    assert team_id == "ti"
