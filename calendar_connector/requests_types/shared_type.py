from typing import TypedDict


class CountryType(TypedDict):
    iso2: str
    name: str


class AvatarType(TypedDict):
    _120x120: str
    medium: str
    field: str
    small: str


class LogoType(TypedDict):
    _168x168: str
    _98x70: str
    _54x54: str


class CoverType(TypedDict):
    _640x414: str
    _170x110: str


class SiteType(TypedDict):
    url: str
    color_primary: str
    color_secondary: str
