from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import create_access_token, hashed_password, verify_password
from app.models.users import User
from app.schemas.user import TokenResponse, UserRegisterRequest, UserLoginRequest



class AuthService:
    async def register(self, db: AsyncSession, data: UserRegisterRequest) -> User:
        existing = await db.scalar(select(User).where(User.username == data.username))
        if existing:
            raise ConflictException("Username already taken")
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password(data.password)
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    async def login(self, db: AsyncSession, username: str, password: str) -> TokenResponse:
        user = await db.scalar(select(User).where(User.username == username))
        if not user:
            raise UnauthorizedException("User not found")
        if not verify_password(password, user.hashed_password):
            raise UnauthorizedException("Invalid password")

        token = create_access_token(
            data = {"sub" : str(user.id), "username" : user.username},
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return TokenResponse(
            access_token = token,
            token_type = "bearer",
            expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User:
        return await db.scalar(select(User).where(User.id == user_id))


auth_service = AuthService()
