import pytest
from app.core.security import hashed_password, verify_password, create_access_token, decode_access_token
from app.core.exceptions import UnauthorizedException

def test_password_hashing():
    hashed = hashed_password("mysecret")
    assert hashed != "mysecret"
    assert verify_password("mysecret", hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_encode_decode():
    token = create_access_token({"sub": "42", "login": "alice"})
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "42"
    assert payload["login"] == "alice"

def test_invalid_token():
    with pytest.raises(UnauthorizedException):
        decode_access_token("not.a.token")
