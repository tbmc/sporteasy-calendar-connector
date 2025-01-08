import base64
import hashlib
import random
import string

from nacl.encoding import HexEncoder
from nacl.public import SealedBox

from calendar_connector.consts import PRESENCE
from calendar_connector.cryptography_key_generation import get_key_cached


def generate_salt() -> str:
    chars: list[str] = []
    for i in range(random.randint(30, 50)):
        chars.append(random.choice(string.printable))
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


def get_public_key_base64() -> str:
    public_key, _ = get_key_cached()
    return base64.b64encode(bytes(public_key)).decode("utf-8")


def encrypt_message(password: str) -> bytes:
    public_key, _ = get_key_cached()
    sealed_box = SealedBox(public_key)
    encrypted = sealed_box.encrypt(password.encode("utf-8"), HexEncoder)
    return encrypted


def decrypt_message(encrypted_password: bytes) -> str:
    _, private_key = get_key_cached()
    unsealed_box = SealedBox(private_key)
    plaintext = unsealed_box.decrypt(encrypted_password, HexEncoder)
    return plaintext.decode("utf-8")
