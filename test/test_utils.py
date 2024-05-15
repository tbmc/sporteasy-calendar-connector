import json
from pathlib import Path
from typing import Any

import pytest

from calendar_connector.normalize import normalize

data_folder = Path(__file__).parent / "data"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("J'aimerais ça. Du pâté !", "J'aimerais ca. Du pate !"),
        ("phrase normale", "phrase normale"),
    ],
)
def test_normalize(test_input, expected) -> None:
    result = normalize(test_input)
    assert expected == result


def read_text_by_name(filename: str) -> str:
    path = data_folder / filename
    with path.open(encoding="utf-8") as f:
        content = f.read()
    return content


def read_json_by_name(filename: str) -> Any:
    return read_json(data_folder / f"{filename}.json")


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        content = f.read()
    return json.loads(content)


def replace_unwanted_lines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\n\n", "\n").strip()
