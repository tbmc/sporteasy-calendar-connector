import json
from pathlib import Path
from typing import Any

data_folder = Path(__file__).parent / "data"


def read_text_by_name(filename: str) -> str:
    path = data_folder / f"{filename}.json"
    with path.open() as f:
        content = f.read()
    return content


def read_json_by_name(filename: str) -> Any:
    return read_json(data_folder / f"{filename}.json")


def read_json(path: Path) -> Any:
    with path.open() as f:
        content = f.read()
    return json.loads(content)
