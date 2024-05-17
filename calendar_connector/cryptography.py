import string
import random
import hashlib

from consts import PRESENCE

_alphabet = string.printable


def generate_salt() -> str:
    chars: list[str] = []
    for i in range(random.randint(30, 50)):
        chars.append(random.choice(_alphabet))
    return "".join(chars)


def generate_hash(
    team_id: int | str,
    event_id: int | str,
    user_id: int | str,
    username: str,
    password: str,
    salt: str,
    presence: bool,
) -> str:
    presence_str = PRESENCE.present if presence else PRESENCE.absent
    to_hash = (
        f"{team_id}:{event_id}:{user_id}:{username}:{password}:{salt}:{presence_str}"
    )
    m = hashlib.sha3_256(to_hash.encode("utf-8"))
    return m.hexdigest()
