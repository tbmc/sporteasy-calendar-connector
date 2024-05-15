from typing import cast

from icalendar import Event

from calendar_connector.consts import EVENT_TYPE, ORDER_PRESENT
from calendar_connector.event_utils.score import extract_scores


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


def extract_event_description(event_data: EVENT_TYPE, event: Event) -> None:
    description = ""
    score = extract_scores(event_data)
    if score is not None:
        description += f"{score}\n"
    attendee = _extract_attendee_description(event_data)
    description += attendee

    event.add("description", description.strip())
