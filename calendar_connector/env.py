from typing import Optional

from dotenv import dotenv_values

_env = dotenv_values(".env")


def load_env_data() -> tuple[str, str, Optional[str]]:
    username = _env.get("username")
    password = _env.get("password")
    team_id = _env.get("team_id")
    assert type(username) is str
    assert type(password) is str

    return username, password, team_id


def load_env_server_private_key() -> str:
    server_private_key = _env.get("SERVER_PRIVATE_KEY")
    if server_private_key is None or server_private_key == "":
        raise Exception("Server private key is empty")
    assert type(server_private_key) is str
    return server_private_key
