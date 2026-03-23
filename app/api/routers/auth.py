from fastapi import APIRouter

from app.schemas.user import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse

router = APIRouter(tags=["auth"])

@router.post("/auth", response_model=UserResponse,status_code=201, summary="Register new user")
async def auth(request: Request):

