from datetime import datetime, timedelta
from typing import Any, cast
import unicodedata

import requests
from icalendar import Calendar, Event, vText
import pytz

session_requests = requests.Session()

url_authenticate = "https://api.sporteasy.net/v2.1/account/authenticate/"
url_list_teams = "https://api.sporteasy.net/v2.1/me/teams/"
url_list_seasons = "https://api.sporteasy.net/v2.1/teams/{team_id}/seasons/"
url_list_events = "https://api.sporteasy.net/v2.1/teams/{team_id}/events/"

PLAYED_WORDS = "played", "present", "available"
EVENT_TYPE = dict[str, int | str | Any | list[Any] | dict[str, Any]]
TIMEZONE = pytz.timezone("UTC")


def normalize(any_str: str) -> str:
    return unicodedata.normalize("NFD", any_str)


def login(username: str, password: str) -> str:
    authenticate_response = session_requests.post(url_authenticate, {
        "username": username,
        "password": password,
    })
    if authenticate_response.status_code != 200:
        raise Exception("Authentication error")
    token: str = authenticate_response.cookies.get("sporteasy")
    # csrf = authenticate_response.cookies.get(csrf_name)
    return token


def list_teams() -> list[tuple[int, str]]:
    response = session_requests.get(url_list_teams)
    data = response.json()
    return [
        (d["id"], normalize(d["name"]))
        for d in data["results"]
    ]


def list_events(team_id: int) -> list[EVENT_TYPE]:
    response = session_requests.get(
        url_list_events.format(team_id=team_id),
        headers={"Accept-Language": "fr-FR"}
    )
    data: list[EVENT_TYPE] = response.json()["results"]
    return data


def event_to_calendar_event(team_id: int, team_name: str, event_data: EVENT_TYPE) -> Event:
    id_ = event_data["id"]

    start_date = datetime.fromisoformat(cast(str, event_data["start_at"]))
    start_date = start_date.astimezone(TIMEZONE)
    end_date_str = cast(str | None, event_data["end_at"])
    if end_date_str is not None:
        end_date = datetime.fromisoformat(end_date_str)
    else:
        end_date = start_date + timedelta(hours=2)
    end_date = end_date.astimezone(TIMEZONE)

    location = normalize(
        cast(
            dict[str, str | Any],
            event_data["location"]
        )["formatted_address"]
    )
    attendance_groups = cast(list[dict[str, int | str]] | None, event_data["attendance_groups"])

    event = Event()
    event.add("uid", str(id_))

    category_name = normalize(
        cast(
            dict[str, str | Any],
            event_data["category"]
        )["localized_name"]
    )
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

    event.add("summary", summary)
    event.add("dtstart", start_date)
    event.add("dtstamp", start_date)
    event.add("dtend", end_date)

    description = ""
    if attendance_groups is not None:
        present_people_count = sum(
            cast(int, ppc["count"])
            for ppc in attendance_groups
            if cast(str, ppc["slug_name"]).lower() in PLAYED_WORDS
        )
        not_present_people_count = sum(
            cast(int, ppc["count"])
            for ppc in attendance_groups
            if cast(str, ppc["slug_name"]).lower() not in PLAYED_WORDS
        )
        description += f"\nPresents: {present_people_count} | Pas presents {not_present_people_count}"

    event.add("description", description)
    event.add("location", location)

    return event


def get_calendar_text(username: str, password: str) -> str:
    login(username, password)
    teams = list_teams()

    cal = Calendar()
    cal.add("summary", vText("SportEasyCalendar"))
    cal.add("prodid", "-//Sporteasy Calendar Connector")
    cal.add("version", "2.0")
    cal.add("vtimezone", "UTC")
    cal.add("calscale", "GREGORIAN")
    cal.add("method", "PUBLISH")
    cal.add("x-wr-calname", "SportEasy Calendar")
    cal.add("x-wr-timezone", "UTC")
    cal.add("x-wr-caldesc", "SportEasy calendar as ics")

    for team_id, team_name in teams:
        events = list_events(team_id)
        for event in events:
            cal.add_component(
                event_to_calendar_event(team_id, team_name, event)
            )

    text_calendar: str = cal \
        .to_ical() \
        .decode("utf-8") \
        .strip() \
        .replace("\r", "\n") \
        .replace("\n\n", "\n")

    return text_calendar


def main() -> None:
    from dotenv import dotenv_values
    env = dotenv_values(".env")

    username = env.get("username")
    password = env.get("password")
    assert type(username) is str
    assert type(password) is str

    calendar_content = get_calendar_text(username, password)
    with open("./test.ics", "w", encoding="utf-8") as f:
        f.write(calendar_content)


if __name__ == "__main__":
    main()
