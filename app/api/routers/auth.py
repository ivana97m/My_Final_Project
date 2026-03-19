from fastapi import APIRouter

router = APIRouter(tags=["auth"])

@router.post("/auth", response_model=schemas.Token)
async def auth(request: Request):

