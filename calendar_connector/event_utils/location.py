from typing import cast, Any

from icalendar import Event

from calendar_connector.consts import EVENT_TYPE
from calendar_connector.normalize import normalize


def extract_event_location(event_data: EVENT_TYPE, event: Event) -> None:
    if event_data is None or event_data["location"] is None:
        return

    location = normalize(
        cast(
            dict[str, str | Any],
            event_data["location"],
        )["formatted_address"]
    )
    event.add("location", location)
