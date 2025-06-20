from datetime import datetime
from typing import cast
from unittest.mock import MagicMock, call

from calendar_connector.consts import TIMEZONE
from calendar_connector.event_utils.date import extract_event_dates
from calendar_connector.requests_types.event_type import EventType


def test_parse_date_event() -> None:
    event_data = cast(
        EventType,
        {
            "start_at": "2023-10-01T04:00:00+02:00",
            "end_at": "2023-10-01T12:00:00+02:00",
        },
    )

    event = MagicMock()

    extract_event_dates(event_data, event)

    assert event.add.call_args_list == [
        call("dtstart", datetime(2023, 10, 1, 2, 0, tzinfo=TIMEZONE)),
        call("dtstamp", datetime(2023, 10, 1, 2, 0, tzinfo=TIMEZONE)),
        call("dtend", datetime(2023, 10, 1, 10, 0, tzinfo=TIMEZONE)),
    ]


def test_parse_date_event_without_end() -> None:
    event_data = cast(
        EventType,
        {
            "start_at": "2023-10-01T04:00:00+02:00",
        },
    )

    event = MagicMock()

    extract_event_dates(event_data, event)

    assert event.add.call_args_list == [
        call("dtstart", datetime(2023, 10, 1, 2, 0, tzinfo=TIMEZONE)),
        call("dtstamp", datetime(2023, 10, 1, 2, 0, tzinfo=TIMEZONE)),
        call("dtend", datetime(2023, 10, 1, 4, 0, tzinfo=TIMEZONE)),
    ]
