from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.schemas.user_schema import UserSignup, UserLogin, TokenResponse, TokenData
from app.database import get_db
from app.models.user import User
from app.auth.jwt_handler import create_access_token
from app.auth.dependencies import get_current_user as get_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def signup(user: UserSignup, db: AsyncSession) -> TokenResponse:
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = pwd_context.hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})

    return TokenResponse(
        data=TokenData(access_token=token), message="User created successfully"
    )


async def login(user: UserLogin, db: AsyncSession) -> TokenResponse:
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return TokenResponse(data=TokenData(access_token=token), message="Login successful")
