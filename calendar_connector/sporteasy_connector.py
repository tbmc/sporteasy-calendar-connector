from typing import NamedTuple

import logging

import requests

from calendar_connector.consts import (
    url_authenticate,
    url_list_teams,
    url_list_events,
    url_put_event_presence,
    url_me,
    url_csrf,
)
from calendar_connector.normalize import normalize
from calendar_connector.requests_types.event_type import EventType
from calendar_connector.requests_types.me_type import MeType
from calendar_connector.requests_types.request_type import RequestType, CsrfType
from calendar_connector.requests_types.team_type import TeamType


class TeamNamedTuple(NamedTuple):
    id: int
    name: str
    web_url: str


team_namedtuple = TeamNamedTuple

logger = logging.getLogger(__name__)


class SporteasyConnector:
    def __init__(self) -> None:
        self.session_requests = requests.Session()
        logger.debug("Initialized SporteasyConnector session")

    def login(self, username: str, password: str) -> str:
        logger.info("Authenticating user=%s", username)
        authenticate_response = self.session_requests.post(
            url_authenticate,
            {
                "username": username,
                "password": password,
            },
        )
        if authenticate_response.status_code != 200:
            logger.warning(
                "Authentication failed for user=%s with status=%s",
                username,
                authenticate_response.status_code,
            )
            raise Exception("Authentication error")
        token: str | None = authenticate_response.cookies.get("sporteasy")
        if token is None:
            logger.error(
                "Authentication succeeded but no token found for user=%s", username
            )
            raise Exception("Authentication error: no token received")

        # csrf = authenticate_response.cookies.get(csrf_name)
        logger.debug("Authentication succeeded for user=%s", username)
        return token

    def list_teams(self) -> list[team_namedtuple]:
        logger.debug("Fetching teams")
        response = self.session_requests.get(url_list_teams)
        if response.status_code != 200:
            logger.warning(
                "Unexpected status while listing teams: %s", response.status_code
            )
        data: RequestType[TeamType] = response.json()
        teams = [
            team_namedtuple(d["id"], normalize(d["name"]), d["web_url"])
            for d in data["results"]
        ]
        logger.info("Fetched %s teams", len(teams))
        return teams

    def list_events(self, team_id: int) -> list[EventType]:
        logger.debug("Fetching events for team_id=%s", team_id)
        response = self.session_requests.get(
            url_list_events.format(team_id=team_id),
            headers={"Accept-Language": "fr-FR"},
        )
        if response.status_code != 200:
            logger.warning(
                "Unexpected status while listing events for team_id=%s: %s",
                team_id,
                response.status_code,
            )
        data: list[EventType] = response.json()["results"]
        logger.debug("Fetched %s events for team_id=%s", len(data), team_id)
        return data

    def get_profile_id(self) -> int:
        logger.debug("Fetching current profile id")
        response = self.session_requests.get(url_me)
        data: MeType = response.json()
        profile_id = data["id"]
        logger.debug("Retrieved profile_id=%s", profile_id)
        return profile_id

    def get_csrf_token(self, team_id: int) -> tuple[str, str]:
        logger.debug("Fetching CSRF token for team_id=%s", team_id)
        response = self.session_requests.get(url_csrf)
        data: CsrfType = response.json()
        csrf = data["csrf_token"]

        teams = self.session_requests.get(url_list_teams).json()["results"]
        current_team = [t for t in teams if t["id"] == team_id][0]
        web_url = current_team["web_url"]  # type: ignore

        logger.debug("Retrieved CSRF token and web_url for team_id=%s", team_id)

        return csrf, web_url

    def put_presence_status(
        self, team_id: int, event_id: int, is_present: bool
    ) -> None:
        logger.info(
            "Updating presence (team_id=%s, event_id=%s, presence=%s)",
            team_id,
            event_id,
            is_present,
        )
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
        if result.status_code >= 400:
            logger.warning(
                "Presence update failed (team_id=%s, event_id=%s, status=%s)",
                team_id,
                event_id,
                result.status_code,
            )
        else:
            logger.info(
                "Presence updated successfully (team_id=%s, event_id=%s)",
                team_id,
                event_id,
            )
