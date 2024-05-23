from typing import cast
import collections

import requests

from calendar_connector.consts import (
    url_authenticate,
    url_list_teams,
    EVENT_TYPE,
    url_list_events,
    url_put_event_presence,
    url_me,
    url_csrf,
)
from calendar_connector.normalize import normalize

team_namedtuple = collections.namedtuple("team_namedtuple", ["id", "name", "web_url"])


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

    def list_teams(self) -> list[team_namedtuple]:
        response = self.session_requests.get(url_list_teams)
        data = response.json()
        return [
            team_namedtuple(d["id"], normalize(d["name"]), d["web_url"])
            for d in data["results"]
        ]

    def list_events(self, team_id: int) -> list[EVENT_TYPE]:
        response = self.session_requests.get(
            url_list_events.format(team_id=team_id),
            headers={"Accept-Language": "fr-FR"},
        )
        data: list[EVENT_TYPE] = response.json()["results"]
        return data

    def get_profile_id(self) -> int:
        response = self.session_requests.get(url_me)
        profile_id = cast(int, response.json()["id"])
        return profile_id

    def get_csrf_token(self, team_id: int) -> tuple[str, str]:
        response = self.session_requests.get(url_csrf)
        csrf = response.json()["csrf_token"]

        teams = self.session_requests.get(url_list_teams).json()["results"]
        current_team = [t for t in teams if t["id"] == team_id][0]
        web_url = current_team["web_url"]  # type: ignore

        return csrf, web_url

    def put_presence_status(
        self, team_id: int, event_id: int, is_present: bool
    ) -> None:
        profile_id = self.get_profile_id()
        csrf, web_url = self.get_csrf_token(team_id)
        formatted_url = url_put_event_presence.format(
            team_id=team_id, event_id=event_id, profile_id=profile_id
        )
        result = self.session_requests.put(
            formatted_url,
            data={"attendance_status": "present" if is_present else "absent"},
            headers={"X-Csrftoken": csrf, "Referer": web_url},
        )
        # print(result)
