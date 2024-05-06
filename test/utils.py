import re
import json
from pathlib import Path
from typing import Any

data_folder = Path(__file__).parent / "data"


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


_SEQUENCE_REGEX = r"(?<=SEQUENCE:)\d+"
_LAST_SYNC_REGEX = r"(?<=\| Last sync: )\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"


def replace_last_sync_and_sequence(text: str) -> str:
    text_sequence = re.sub(_SEQUENCE_REGEX, "173512350", text)
    text_date = re.sub(_LAST_SYNC_REGEX, "2024-12-25 10:45:00", text_sequence)
    return text_date
