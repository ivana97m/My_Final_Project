from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.exceptions import ConflictException, UnauthorizedException
from app.models.users import User
from app.schemas.user import UserRegisterRequest
from app.services.auth_service import AuthService


FAKE_HASH = "$2b$12$fakehashfortesting00000000000000000000000000000000"


def make_user(
    login: str = "testuser",
    email: str | None = None,
    is_active: bool = True,
) -> User:
    user = User()
    user.id = 1
    user.login = login
    user.email = email
    user.hashed_password = FAKE_HASH
    user.is_active = is_active
    return user


@pytest.fixture
def service() -> AuthService:
    return AuthService()


@pytest.fixture
def mock_db() -> AsyncMock:
    db = AsyncMock()
    db.add = MagicMock()
    return db


@pytest.mark.asyncio
async def test_register_success(service: AuthService, mock_db: AsyncMock):
    mock_db.scalar.return_value = None
    mock_db.flush = AsyncMock()
    mock_db.refresh = AsyncMock()

    data = UserRegisterRequest(
        login="newuser",
        password="password123",
        repeat_password="password123",
        email="newuser@example.com",
    )

    with patch("app.services.auth_service.hash_password", return_value="hashed"):
        user = await service.register(mock_db, data)

    mock_db.add.assert_called_once()
    mock_db.flush.assert_called_once()
    mock_db.refresh.assert_called_once()

    created_user = mock_db.add.call_args[0][0]
    assert created_user.login == "newuser"
    assert created_user.hashed_password == "hashed"


@pytest.mark.asyncio
async def test_register_with_email(service: AuthService, mock_db: AsyncMock):
    mock_db.scalar.return_value = None
    mock_db.flush = AsyncMock()
    mock_db.refresh = AsyncMock()

    data = UserRegisterRequest(
        login="newuser",
        password="password123",
        repeat_password="password123",
        email="user@example.com",
    )

    with patch("app.services.auth_service.hash_password", return_value="hashed"):
        await service.register(mock_db, data)

    created_user = mock_db.add.call_args[0][0]
    assert created_user.email == "user@example.com"


@pytest.mark.asyncio
async def test_register_duplicate_login(service: AuthService, mock_db: AsyncMock):
    mock_db.scalar.return_value = make_user("existinguser")

    data = UserRegisterRequest(
        login="existinguser",
        password="password123",
        repeat_password="password123",
        email="existing@example.com",
    )

    with pytest.raises(ConflictException):
        await service.register(mock_db, data)


@pytest.mark.asyncio
async def test_login_success(service: AuthService, mock_db: AsyncMock):
    mock_db.scalar.return_value = make_user("testuser")

    with patch("app.services.auth_service.verify_password", return_value=True):
        result = await service.login(mock_db, "testuser", "password123")

    assert result.access_token is not None
    assert result.token_type == "bearer"
    assert result.expires_in == 3600


@pytest.mark.asyncio
async def test_login_wrong_password(service: AuthService, mock_db: AsyncMock):
    mock_db.scalar.return_value = make_user("testuser")

    with patch("app.services.auth_service.verify_password", return_value=False):
        with pytest.raises(UnauthorizedException):
            await service.login(mock_db, "testuser", "wrongpassword")


@pytest.mark.asyncio
async def test_login_empty_password(service: AuthService, mock_db: AsyncMock):
    mock_db.scalar.return_value = make_user("testuser")

    with patch("app.services.auth_service.verify_password", return_value=False):
        with pytest.raises(UnauthorizedException):
            await service.login(mock_db, "testuser", "")


@pytest.mark.asyncio
async def test_login_user_not_found(service: AuthService, mock_db: AsyncMock):
    mock_db.scalar.return_value = None

    with pytest.raises(UnauthorizedException):
        await service.login(mock_db, "ghostuser", "password123")


@pytest.mark.asyncio
async def test_login_inactive_user(service: AuthService, mock_db: AsyncMock):
    mock_db.scalar.return_value = make_user("testuser", is_active=False)

    with patch("app.services.auth_service.verify_password", return_value=True):
        with pytest.raises(UnauthorizedException):
            await service.login(mock_db, "testuser", "password123")


@pytest.mark.asyncio
async def test_get_user_by_id_found(service: AuthService, mock_db: AsyncMock):
    expected = make_user()
    mock_db.scalar.return_value = expected

    result = await service.get_user_by_id(mock_db, 1)

    assert result == expected


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(service: AuthService, mock_db: AsyncMock):
    mock_db.scalar.return_value = None

    result = await service.get_user_by_id(mock_db, 999)

    assert result is None