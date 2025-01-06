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
