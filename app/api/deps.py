from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedException
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.users import User
from app.services.auth_service import auth_service


security = HTTPBearer()

async def get_current_user (
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)]
)-> User:
    payload = decode_access_token(credentials.credentials)
    if not payload or "sub" not in payload:
        raise UnauthorizedException("Invalid or expired token")

    user_id = int(payload["sub"])
    user = await auth_service.get_user_by_id(db, user_id)
    if not user:
        raise UnauthorizedException("User not found")
    return user

CurrentUser = Annotated[User,Depends(get_current_user)]
DB = Annotated[AsyncSession,Depends(get_db)]