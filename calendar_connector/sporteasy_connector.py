import requests

from calendar_connector.consts import (
    url_authenticate,
    url_list_teams,
    EVENT_TYPE,
    url_list_events,
)
from calendar_connector.normalize import normalize


class SporteasyConnector:
    def __init__(self) -> None:
        self.session_requests = requests.Session()

    def login(self, username: str, password: str) -> str:
        authenticate_response = self.session_requests.post(
            url_authenticate,
            {
                "username": username,
                "password": password,
            },
        )
        if authenticate_response.status_code != 200:
            raise Exception("Authentication error")
        token: str = authenticate_response.cookies.get("sporteasy")
        # csrf = authenticate_response.cookies.get(csrf_name)
        return token

    def list_teams(self) -> list[tuple[int, str]]:
        response = self.session_requests.get(url_list_teams)
        data = response.json()
        return [(d["id"], normalize(d["name"])) for d in data["results"]]

    def list_events(self, team_id: int) -> list[EVENT_TYPE]:
        response = self.session_requests.get(
            url_list_events.format(team_id=team_id),
            headers={"Accept-Language": "fr-FR"},
        )
        data: list[EVENT_TYPE] = response.json()["results"]
        return data
