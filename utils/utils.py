import unicodedata


def normalize(any_str: str) -> str:
    normalized = unicodedata.normalize("NFKD", any_str)
    # Remove accent by removing combining character after each character
    # Example: "é" => "e" + "'́"
    return "".join([c for c in normalized if not unicodedata.combining(c)])
