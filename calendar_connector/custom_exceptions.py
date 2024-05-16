class AttributeNotFoundException(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"{name} is not found")


class BadTokenException(Exception):
    def __init__(self) -> None:
        super().__init__(f"Your token is not valid")
