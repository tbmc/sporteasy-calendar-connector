import requests_mock

from calendar_connector.sporteasy_connector import SporteasyConnector, team_namedtuple
from test.test_utils import read_text_by_name
from calendar_connector.consts import url_list_teams


def test_list_teams() -> None:
    mocked_response = read_text_by_name("list_teams.json")
    with requests_mock.Mocker() as m:
        m.get(url_list_teams, text=mocked_response)

        connector = SporteasyConnector()
        result = connector.list_teams()

    assert result == [
        team_namedtuple(1, "Equipe 1", "https://equipe1.sporteasy.net/"),
        team_namedtuple(2, "Equipe 2", "https://equipe2.sporteasy.net/"),
    ]
