from unittest.mock import patch, MagicMock

from calendar_connector.cryptography import encrypt_message, decrypt_message


@patch(
    "calendar_connector.cryptography_key_generation.load_env_server_private_key",
    return_value="key_test",
)
def test_libsodium_encrypt_decrypt(mock_load_key: MagicMock) -> None:
    data = "password_test"
    encrypted = encrypt_message(data)
    print(encrypted)
    decrypted = decrypt_message(encrypted)
    assert data == decrypted
    mock_load_key.assert_called_once()
