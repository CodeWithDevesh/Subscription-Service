from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import UserSignup, UserLogin, TokenResponse
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user as get_user
from app.schemas.user_schema import User_Response
from app.services.auth_service import signup as signup_service, login as login_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=TokenResponse)
async def signup(user: UserSignup, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    return await signup_service(user, db)


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    return await login_service(user, db)


@router.get("/me", response_model=User_Response)
async def get_current_user(user: User = Depends(get_user)):
    return User_Response(
        data=user,
        message="User retrieved successfully"
    )
