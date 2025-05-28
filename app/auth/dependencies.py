from fastapi import Depends, HTTPException
from app.auth.auth_bearer import JWTBearer
from app.database import get_db
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_current_user(
    user_id: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_db)
) -> User:
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
