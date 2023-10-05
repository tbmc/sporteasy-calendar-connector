import unicodedata


def normalize(any_str: str) -> str:
    return unicodedata.normalize("NFD", any_str)
