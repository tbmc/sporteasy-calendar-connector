from datetime import datetime
from typing import Optional

from icalendar import Event

from calendar_connector.datetime_utils import get_current_timestamp
from calendar_connector.event_utils.date import extract_event_dates
from calendar_connector.event_utils.description import (
    extract_event_description,
    GenerateLinksData,
)
from calendar_connector.event_utils.location import extract_event_location
from calendar_connector.event_utils.summary import extract_event_summary
from calendar_connector.normalize import normalize
from calendar_connector.types.event_type import EventType


def event_to_calendar_event(
    team_id: int,
    team_name: str,
    event_data: EventType,
    links_data: Optional[GenerateLinksData],
    team_web_url: str,
) -> Event:
    event = Event()
    event.add("uid", str(event_data["id"]) + f"@sporteasy.net")
    extract_event_location(event_data, event)
    extract_event_dates(event_data, event)
    extract_event_summary(event_data, event, team_name)
    extract_event_description(team_id, event_data, event, links_data, team_web_url)

    event.add("class", "PUBLIC")
    current_timestamp = get_current_timestamp()
    event.add("sequence", current_timestamp)
    event.add("transp", "OPAQUE")

    # todo: change this if possible
    event.add("created", datetime(2020, 1, 1, 1, 1, 1))
    event.add("last-modified", datetime(2020, 1, 1, 1, 1, 1))

    category_name = normalize(event_data["category"]["localized_name"])

    return event
