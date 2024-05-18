import os
import datetime
import importlib
from pathlib import Path
from unittest.mock import patch, MagicMock

import requests_mock

import calendar_connector.event_convertor
import calendar_connector.calendar_converter
from calendar_connector.consts import url_list_events, url_list_teams, url_authenticate
from database.create_tables import create_db
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
def test_get_calendar_text_without_links(
    timestamp_mock: MagicMock,
    datetime_mock: MagicMock,
) -> None:
    importlib.reload(calendar_connector.calendar_converter)
    importlib.reload(calendar_connector.event_convertor)

    mocked_response_teams = read_text_by_name("list_teams.json")
    mocked_response_events = read_text_by_name("list_events.json")

    expected_calendar = replace_unwanted_lines(
        read_text_by_name("expected_calendar_without_links.ics")
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
        calendar_text = converter.get_calendar_text(
            "username", "password", False, "http://localhost:5000/", "1"
        )

    result = replace_unwanted_lines(calendar_text)
    assert result == expected_calendar


@patch(
    "calendar_connector.datetime_utils.get_current_timestamp", return_value=173512350
)
@patch(
    "calendar_connector.datetime_utils.get_current_datetime",
    return_value=datetime.datetime(2024, 12, 25, 10, 45, 0),
)
@patch("calendar_connector.cryptography.generate_salt", return_value="salt")
def test_get_calendar_text_with_links(
    timestamp_mock: MagicMock,
    datetime_mock: MagicMock,
    generate_salt_mock: MagicMock,
) -> None:
    db_path = Path(__file__).parent / "data" / "test.db"
    if db_path.exists():
        os.remove(db_path)

    db = create_db()

    importlib.reload(calendar_connector.calendar_converter)
    importlib.reload(calendar_connector.event_convertor)

    mocked_response_teams = read_text_by_name("list_teams.json")
    mocked_response_events = read_text_by_name("list_events.json")

    expected_calendar = replace_unwanted_lines(
        read_text_by_name("expected_calendar_with_links.ics")
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
        calendar_text = converter.get_calendar_text(
            "username", "password", True, "http://localhost:5000/", "1"
        )

    os.remove(db_path)

    result = replace_unwanted_lines(calendar_text)
    assert result == expected_calendar
