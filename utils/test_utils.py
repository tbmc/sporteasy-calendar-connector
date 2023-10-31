import pytest

from .utils import normalize


@pytest.mark.parametrize("test_input,expected", [
    ("J'aimerais ça. Du pâté !", "J'aimerais ca. Du pate !"),
    ("phrase normale", "phrase normale"),
])
def test_normalize(test_input, expected) -> None:
    result = normalize(test_input)
    assert expected == result
