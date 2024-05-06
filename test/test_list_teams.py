import requests_mock

from test.utils import read_text_by_name
from utils.calendar_converter import CalendarConverter
from utils.consts import url_list_teams


def test_list_teams() -> None:
    mocked_response = read_text_by_name('list_teams')
    with requests_mock.Mocker() as m:
        m.get(url_list_teams, text=mocked_response)

        converter = CalendarConverter()
        result = converter.list_teams()

    assert result == [
        (1, "Equipe 1"),
        (2, "Equipe 2"),
    ]
