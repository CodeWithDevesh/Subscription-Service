from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.schemas.subscription_schema import SubscriptionCreate
from app.services.sub_service import get_subs, update_subs, cancel_subs, create_subs

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("/")
async def create_subscription(
    data: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await create_subs(user.id, data, db)


@router.get("/{user_id}")
async def get_user_subscription(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return await get_subs(user_id, db)


@router.get("/")
async def get_subscription(
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    return await get_subs(user.id, db)


@router.put("/{user_id}")
async def update_user_subscription(
    user_id: int,
    data: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return await update_subs(user_id, data, db)


@router.put("/")
async def update_subscription(
    data: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await update_subs(user.id, data, db)


@router.delete("/{user_id}")
async def cancel_user_subscription(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return await cancel_subs(user_id, db)


@router.delete("/")
async def cancel_subscription(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await cancel_subs(user.id, db)
