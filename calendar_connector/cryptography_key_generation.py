from typing import Optional
from nacl.public import PublicKey, PrivateKey
from nacl.hash import sha256
from nacl.encoding import RawEncoder
from calendar_connector.env import load_env_server_private_key


def _get_keys(server_private_key: str) -> tuple[PublicKey, PrivateKey]:
    hashed = sha256(server_private_key.encode("utf-8"), encoder=RawEncoder)
    private_key = PrivateKey(hashed)
    return private_key.public_key, private_key


_public_key_cache: Optional[PublicKey] = None
_private_key_cache: Optional[PrivateKey] = None


def get_key_cached() -> tuple[PublicKey, PrivateKey]:
    global _public_key_cache, _private_key_cache

    if _public_key_cache is not None and _private_key_cache is not None:
        return _public_key_cache, _private_key_cache

    server_private_key = load_env_server_private_key()
    _public_key_cache, _private_key_cache = _get_keys(server_private_key)
    return _public_key_cache, _private_key_cache
