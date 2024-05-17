from typing import Optional


class AttributeNotFoundException(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"{name} is not found")


class BadTokenException(Exception):
    def __init__(self) -> None:
        super().__init__(f"Your token is not valid")


class TooManyUsersException(Exception):
    def __init__(self, mail: str, n: Optional[int] = None) -> None:
        super().__init__(
            f'There are too many users with the same mail "{mail}", this should not happen.'
            + ("" if n is None else f"Number of users {n}.")
        )
