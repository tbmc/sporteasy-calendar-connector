from typing import Optional

from icalendar import Event

from calendar_connector.normalize import normalize
from calendar_connector.types.event_type import EventType


def extract_event_location(event_data: Optional[EventType], event: Event) -> None:
    if event_data is None or event_data["location"] is None:
        return

    location = normalize(event_data["location"]["formatted_address"])
    event.add("location", location)
