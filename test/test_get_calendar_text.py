import datetime
import importlib
from unittest.mock import patch, MagicMock

import requests_mock

import calendar_connector.calendar_converter
from calendar_connector.consts import url_list_events, url_list_teams, url_authenticate
from .test_utils import (
    read_text_by_name,
    replace_unwanted_lines,
)


@patch(
    "calendar_connector.datetime_utils.get_current_timestamp", return_value=173512350
)
@patch(
    "calendar_connector.datetime_utils.get_current_datetime",
    return_value=datetime.datetime(2024, 12, 25, 10, 45, 0),
)
def test_get_calendar_text(
    timestamp_mock: MagicMock,
    datetime_mock: MagicMock,
) -> None:
    importlib.reload(calendar_connector.calendar_converter)

    mocked_response_teams = read_text_by_name("list_teams.json")
    mocked_response_events = read_text_by_name("list_events.json")

    expected_calendar = replace_unwanted_lines(
        read_text_by_name("expected_calendar.ics")
    )

    with requests_mock.Mocker() as request_mocker:
        request_mocker.post(
            url_authenticate,
            status_code=200,
            cookies={"sporteasy": "token test calendar"},
        )
        request_mocker.get(url_list_teams, text=mocked_response_teams)
        request_mocker.get(
            url_list_events.format(team_id=1), text=mocked_response_events
        )

        converter = calendar_connector.calendar_converter.CalendarConverter()
        calendar_text = converter.get_calendar_text("username", "password", "1")

    result = replace_unwanted_lines(calendar_text)
    assert result == expected_calendar
