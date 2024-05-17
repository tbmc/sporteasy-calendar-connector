import dataclasses
from typing import cast, Optional

from icalendar import Event

from calendar_connector.consts import (
    EVENT_TYPE,
    ORDER_PRESENT,
    route_change_presence,
    PRESENCE,
)
from calendar_connector.datetime_utils import get_formated_current_time
from calendar_connector.event_utils.score import extract_scores
from calendar_connector.cryptography import generate_hash


@dataclasses.dataclass
class GenerateLinksData:
    user_id: int
    username: str
    password: str
    salt: str
    url_root: str


def _extract_attendee_description(event_data: EVENT_TYPE) -> str:
    attendance_groups = cast(
        list[dict[str, int | str]] | None, event_data["attendance_groups"]
    )
    attendee = ""
    if attendance_groups is not None:
        attendance_group_list: list[tuple[int, str, int]] = []
        for ppc in attendance_groups:
            slug_sort_value = ORDER_PRESENT.get(cast(str, ppc["slug_name"]), 0)
            attendance_group_list.append(
                (
                    slug_sort_value,
                    cast(str, ppc["localized_name"]),
                    cast(int, ppc["count"]),
                )
            )
        attendance_group_list.sort(reverse=True)

        attendee = ", ".join(
            [
                f"{localized_name}: {count}"
                for _, localized_name, count in attendance_group_list
            ]
        )

    return attendee


def _generate_response_links(
    team_id: int, event_id: int, data: GenerateLinksData
) -> str:
    hashed_present = generate_hash(
        team_id,
        event_id,
        data.user_id,
        data.username,
        data.password,
        data.salt,
        True,
    )
    hashed_absent = generate_hash(
        team_id,
        event_id,
        data.user_id,
        data.username,
        data.password,
        data.salt,
        False,
    )
    url = (
        f"{data.url_root}{route_change_presence[1:]}"
        f"?team_id={team_id}&event_id={event_id}&user_id={data.user_id}"
    )
    present = f'<a href="{url}&token={hashed_present}&presence={PRESENCE.present}">Present</a>'
    absent = (
        f'<a href="{url}&token={hashed_absent}&presence={PRESENCE.absent}">Absent</a>'
    )

    return f"{present} | {absent}"


def extract_event_description(
    team_id: int,
    event_data: EVENT_TYPE,
    event: Event,
    links_data: Optional[GenerateLinksData],
) -> None:
    description = ""
    score = extract_scores(event_data)
    if score is not None:
        description += f"{score}\n"
    attendee = _extract_attendee_description(event_data)
    description += f"{attendee}\n"

    if links_data:
        event_id = cast(int, event_data["id"])
        response_links = _generate_response_links(team_id, event_id, links_data)
        description += f"{response_links}\n"

    description += f"\nLast sync: {get_formated_current_time()}\n"

    event.add("description", description.strip())
