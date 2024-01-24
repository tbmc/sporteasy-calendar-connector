import time
from datetime import datetime, timedelta
from typing import Any, cast, Literal

import requests
from icalendar import Calendar, Event, vText

from utils.consts import EVENT_TYPE, TIMEZONE, MY_PRESENCE, ORDER_PRESENT, url_authenticate, url_list_teams, \
    url_list_events
from utils.env import load_env_data
from utils.utils import normalize


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


def _status_to_ics_status(sp_status: str) -> str:
    sp_status = sp_status.upper()
    if sp_status == "CONFIRMED":
        return "CONFIRMED"
    if sp_status == "CANCELLED":
        return "CANCELLED"
    if sp_status == "NEEDS-ACTION":
        return "TENTATIVE"
    return sp_status


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
        event.add("status", _status_to_ics_status(presence))

    event.add("summary", summary)


def _extract_attendee_description(event_data: EVENT_TYPE) -> str:
    attendance_groups = cast(list[dict[str, int | str]] | None, event_data["attendance_groups"])
    attendee = ""
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

        attendee = ", ".join([
            f"{localized_name}: {count}"
            for _, localized_name, count in attendance_group_list
        ])

    return attendee


def _extract_scores_for_opponent(event_data: EVENT_TYPE, left_or_right: Literal["left", "right"]) \
        -> tuple[str, int] | None:
    opponent = event_data.get(f"opponent_{left_or_right}")
    if opponent is None:
        return None
    score_str = opponent.get("score")
    if score_str is None:
        return None
    name = cast(str, opponent.get("short_name"))
    score = int(cast(str, score_str))
    return name, score


def _extract_scores(event_data: EVENT_TYPE) -> str | None:
    left = _extract_scores_for_opponent(event_data, "left")
    right = _extract_scores_for_opponent(event_data, "right")

    if left is None or right is None:
        return None

    left_name, left_score = left
    right_name, right_score = right
    return f"{left_name} {left_score} - {right_score} {right_name}"


def _extract_event_description(event_data: EVENT_TYPE, event: Event) -> None:
    description = ""
    score = _extract_scores(event_data)
    if score is not None:
        description += f"{score}\n"
    attendee = _extract_attendee_description(event_data)
    description += attendee

    event.add("description", description.strip())


def event_to_calendar_event(team_name: str, event_data: EVENT_TYPE) -> Event:
    event = Event()
    event.add("uid", str(event_data["id"]) + f"@sporteasy.net")
    _extract_event_location(event_data, event)
    _extract_event_dates(event_data, event)
    _extract_event_summary(event_data, event, team_name)
    _extract_event_description(event_data, event)

    event.add("class", "PUBLIC")
    current_timestamp = int(time.time() / 10)
    event.add("sequence", current_timestamp)
    event.add("transp", "OPAQUE")

    # todo: change this if possible
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
        cal.add("REFRESH-INTERVAL;VALUE=DURATION", "PT8H")
        cal.add("X-PUBLISHED-TTL", "PT8H")

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


def main() -> None:
    username, password, team_id = load_env_data()

    calendar_converter = CalendarConverter()
    calendar_content = calendar_converter.get_calendar_text(username, password, team_id)
    with open("./test.ics", "w", encoding="utf-8") as f:
        f.write(calendar_content)


if __name__ == "__main__":
    main()
