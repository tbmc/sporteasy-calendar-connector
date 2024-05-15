from datetime import datetime, timedelta
from typing import cast

from icalendar import Event

from calendar_connector.consts import EVENT_TYPE, TIMEZONE


def extract_event_dates(event_data: EVENT_TYPE, event: Event) -> None:
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
