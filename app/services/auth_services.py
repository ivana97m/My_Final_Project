from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import TokenResponse, UserRegisterRequest

class AuthService:
    async def register(self, db: AsyncSession, data: UserRegisterRequest) -> User:
        existing = await db.scalar(select(User).where(User.login == data.login))
        if existing:
            raise ConflictException("Login already taken")
