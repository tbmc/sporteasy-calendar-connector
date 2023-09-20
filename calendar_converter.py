from datetime import datetime, timedelta
from typing import Any, cast
import unicodedata

import requests
from icalendar import Calendar, Event, vText
import pytz
from dotenv import dotenv_values

url_authenticate = "https://api.sporteasy.net/v2.1/account/authenticate/"
url_list_teams = "https://api.sporteasy.net/v2.1/me/teams/"
url_list_seasons = "https://api.sporteasy.net/v2.1/teams/{team_id}/seasons/"
url_list_events = "https://api.sporteasy.net/v2.1/teams/{team_id}/events/"

PLAYED_WORDS = "played", "present", "available"
EVENT_TYPE = dict[str, int | str | Any | list[Any] | dict[str, Any]]
TIMEZONE = pytz.timezone("UTC")

ORDER_PRESENT = {
    "available": 50,
    "played": 51,
    "present": 52,
    "rsvp": 40,
    "not_selected": 30,
    "unavailable": 10,
    "not_played": 11,
}

MY_PRESENCE = {
    "available": "CONFIRMED",
    "played": "CONFIRMED",
    "present": "CONFIRMED",
    "rsvp": "NEEDS-ACTION",
    "not_selected": "CANCELLED",
    "unavailable": "CANCELLED",
    "not_played": "CANCELLED",
}


def normalize(any_str: str) -> str:
    return unicodedata.normalize("NFD", any_str)


def _extract_event_dates(event_data: EVENT_TYPE, event: Event) -> None:
    start_date = datetime.fromisoformat(cast(str, event_data["start_at"]))
    start_date = start_date.astimezone(TIMEZONE)
    end_date_str = cast(str | None, event_data["end_at"])
    if end_date_str is not None:
        end_date = datetime.fromisoformat(end_date_str)
    else:
        end_date = start_date + timedelta(hours=2)
    end_date = end_date.astimezone(TIMEZONE)

    event.add("dtstart", start_date)
    event.add("dtstamp", start_date)
    event.add("dtend", end_date)


def _extract_event_location(event_data: EVENT_TYPE, event: Event) -> None:
    if event_data is None or event_data["location"] is None:
        return

    location = normalize(
        cast(
            dict[str, str | Any],
            event_data["location"],
        )["formatted_address"]
    )
    event.add("location", location)


def _extract_event_summary(event_data: EVENT_TYPE, event: Event, team_name: str) -> None:
    name = normalize(cast(str, event_data["name"]))
    if team_name not in name:
        summary = f"{team_name} - {name}"
    else:
        summary = name

    # opponent_right = cast(dict[str, int | str | None] | None, event_data["opponent_right"])
    # opponent_left = cast(dict[str, int | str | None] | None, event_data["opponent_left"])
    # if opponent_left is not None and opponent_right is not None:
    #     if opponent_left["id"] == team_id:
    #         opponent_name = opponent_right["short_name"]
    #     else:
    #         opponent_name = opponent_left["short_name"]
    #     summary += f" - contre {opponent_name}"

    me_object = event_data.get("me", {})
    if me_object is not None and me_object.get("group") is not None:
        group = cast(dict[str, str], me_object.get("group", {}))
        localized_name_presence = group.get("localized_name")
        if localized_name_presence is not None:
            summary += f" - {normalize(localized_name_presence)}"

        slug_presence = group.get("slug_name")
        presence = MY_PRESENCE.get(slug_presence)
        event.add("status", presence)

    event.add("summary", summary)


def _extract_event_description(event_data: EVENT_TYPE, event: Event) -> None:
    attendance_groups = cast(list[dict[str, int | str]] | None, event_data["attendance_groups"])
    description = ""
    if attendance_groups is not None:
        attendance_group_list: list[tuple[int, str, int]] = []
        for ppc in attendance_groups:
            slug_sort_value = ORDER_PRESENT.get(cast(str, ppc["slug_name"]), 0)
            attendance_group_list.append((
                slug_sort_value,
                cast(str, ppc["localized_name"]),
                cast(int, ppc["count"])
            ))
        attendance_group_list.sort(reverse=True)

        description = ", ".join([
            f"{localized_name}: {count}"
            for _, localized_name, count in attendance_group_list
        ])

    event.add("description", description.strip())


def event_to_calendar_event(team_name: str, event_data: EVENT_TYPE) -> Event:
    event = Event()
    event.add("uid", str(event_data["id"]) + "@sporteasy.net")
    _extract_event_location(event_data, event)
    _extract_event_dates(event_data, event)
    _extract_event_summary(event_data, event, team_name)
    _extract_event_description(event_data, event)

    event.add("class", "PUBLIC")
    event.add("sequence", 0)
    event.add("transp", "OPAQUE")

    # todo: change this
    event.add("created", datetime(2020, 1, 1, 1, 1, 1))
    event.add("last-modified", datetime(2020, 1, 1, 1, 1, 1))

    category_name = normalize(
        cast(
            dict[str, str | Any],
            event_data["category"]
        )["localized_name"]
    )

    return event


class CalendarConverter:
    def __init__(self) -> None:
        self.session_requests = requests.Session()

    def login(self, username: str, password: str) -> str:
        authenticate_response = self.session_requests.post(url_authenticate, {
            "username": username,
            "password": password,
        })
        if authenticate_response.status_code != 200:
            raise Exception("Authentication error")
        token: str = authenticate_response.cookies.get("sporteasy")
        # csrf = authenticate_response.cookies.get(csrf_name)
        return token

    def list_teams(self) -> list[tuple[int, str]]:
        response = self.session_requests.get(url_list_teams)
        data = response.json()
        return [
            (d["id"], normalize(d["name"]))
            for d in data["results"]
        ]

    def list_events(self, team_id: int) -> list[EVENT_TYPE]:
        response = self.session_requests.get(
            url_list_events.format(team_id=team_id),
            headers={"Accept-Language": "fr-FR"}
        )
        data: list[EVENT_TYPE] = response.json()["results"]
        return data

    def get_calendar_text(self, username: str, password: str, team_id: str | None = None) -> str:
        self.login(username, password)
        teams = self.list_teams()

        cal = Calendar()
        cal.add("summary", vText("SportEasyCalendar"))
        cal.add("prodid", "-//Sporteasy Calendar Connector")
        cal.add("version", "2.0")
        cal.add("vtimezone", "UTC")
        cal.add("calscale", "GREGORIAN")
        cal.add("method", "PUBLISH")
        cal.add("x-wr-calname", "SportEasy Calendar")
        cal.add("x-wr-timezone", "Europe/Paris")
        cal.add("x-wr-caldesc", "SportEasy calendar as ics")

        for current_team_id, team_name in teams:
            # Ignore other teams
            if team_id is not None and team_id != "" and int(team_id) != current_team_id:
                continue
            events = self.list_events(current_team_id)
            for event in events:
                cal.add_component(
                    event_to_calendar_event(team_name, event)
                )

        text_calendar: str = cal \
            .to_ical() \
            .decode("utf-8") \
            .strip()

        return text_calendar


def load_env_data() -> tuple[str, str, str]:
    env = dotenv_values(".env")

    username = env.get("username")
    password = env.get("password")
    team_id = env.get("team_id")
    assert type(username) is str
    assert type(password) is str

    return username, password, team_id


def main() -> None:
    username, password, team_id = load_env_data()

    calendar_converter = CalendarConverter()
    calendar_content = calendar_converter.get_calendar_text(username, password, team_id)
    with open("./test.ics", "w", encoding="utf-8") as f:
        f.write(calendar_content)


if __name__ == "__main__":
    main()
