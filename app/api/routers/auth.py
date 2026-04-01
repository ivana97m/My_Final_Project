from fastapi import APIRouter

from app.api.deps import DB
from app.schemas.user import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.services.auth_service import auth_service

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserResponse,status_code=201, summary="Register new user")
async def register (data: UserRegisterRequest, db: DB) -> UserResponse:
    user = await auth_service.register(db, data)
    return UserResponse.model_validate(user)

@router.post("/login", response_model=TokenResponse, status_code=200, summary="Log In")
async def login (data: UserLoginRequest, db: DB) -> TokenResponse:
    return await auth_service.login(db, data.username, data.password)

