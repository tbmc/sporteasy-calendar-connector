import requests_mock

from utils.calendar_converter import CalendarConverter
from utils.consts import url_authenticate


def test_login() -> None:
    with requests_mock.Mocker() as m:
        m.post(url_authenticate, status_code=200, cookies={"sporteasy": "token test"})

        converter = CalendarConverter()
        token = converter.login("username", "password")

    assert token == "token test"
