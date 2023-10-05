from dotenv import dotenv_values

env = dotenv_values(".env")


def load_env_data() -> tuple[str, str, str]:
    username = env.get("username")
    password = env.get("password")
    team_id = env.get("team_id")
    assert type(username) is str
    assert type(password) is str

    return username, password, team_id
