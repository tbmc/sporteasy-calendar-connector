import requests_mock

from test.utils import (
    read_text_by_name,
    replace_unwanted_lines,
    replace_last_sync_and_sequence,
)
from utils.calendar_converter import CalendarConverter
from utils.consts import url_list_events, url_list_teams, url_authenticate


def test_get_calendar_text() -> None:
    mocked_response_teams = read_text_by_name("list_teams.json")
    mocked_response_events = read_text_by_name("list_events.json")

    expected_calendar = replace_unwanted_lines(
        read_text_by_name("expected_calendar.ics")
    )

    with requests_mock.Mocker() as m:
        m.post(
            url_authenticate,
            status_code=200,
            cookies={"sporteasy": "token test calendar"},
        )
        m.get(url_list_teams, text=mocked_response_teams)
        m.get(url_list_events.format(team_id=1), text=mocked_response_events)

        converter = CalendarConverter()
        calendar_text = converter.get_calendar_text("username", "password", "1")

    result = replace_last_sync_and_sequence(replace_unwanted_lines(calendar_text))
    assert result == expected_calendar
