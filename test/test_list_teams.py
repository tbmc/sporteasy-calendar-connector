import requests_mock

from calendar_connector.sporteasy_connector import SporteasyConnector
from test.test_utils import read_text_by_name
from calendar_connector.calendar_converter import CalendarConverter
from calendar_connector.consts import url_list_teams


def test_list_teams() -> None:
    mocked_response = read_text_by_name("list_teams.json")
    with requests_mock.Mocker() as m:
        m.get(url_list_teams, text=mocked_response)

        connector = SporteasyConnector()
        result = connector.list_teams()

    assert result == [
        (1, "Equipe 1"),
        (2, "Equipe 2"),
    ]
