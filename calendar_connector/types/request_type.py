from typing import TypedDict, TypeVar, Generic

T = TypeVar("T")


class RequestType(TypedDict, Generic[T]):
    count: int
    links: dict[str, str]
    results: list[T]


class CsrfType(TypedDict):
    csrf_token: str
