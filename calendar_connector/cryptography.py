import string
import random
import hashlib

_alphabet = string.printable


def generate_salt() -> str:
    chars: list[str] = []
    for i in range(random.randint(30, 50)):
        chars.append(random.choice(_alphabet))
    return "".join(chars)


def hash_string(s: str) -> str:
    m = hashlib.sha3_256(s.encode("utf-8"))
    return m.hexdigest()


def generate_hash(
    event_id: str, user_id: int | str, username: str, password: str, salt: str
) -> str:
    hashed = hash_string(f"{event_id}:{user_id}:{username}:{password}:{salt}")
    return hashed
