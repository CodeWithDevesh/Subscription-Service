from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.schemas.subscription_schema import (
    SubscriptionCreate,
    SubscriptionResponse,
    SubscriptionHistory,
)
from app.services.sub_service import (
    get_subs,
    update_subs,
    cancel_subs,
    create_subs,
    get_subs_history,
    get_active_subs,
)

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("/", response_model=SubscriptionResponse)
async def create_subscription(
    data: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    "Subscribe to a plan"
    return await create_subs(user.id, data, db)


@router.get("/active", response_model=SubscriptionHistory)
async def get_active_subscriptions(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    "Get all active subscriptions (admin only)"
    return await get_active_subs(db)


@router.get("/history/{user_id}", response_model=SubscriptionHistory)
async def get_user_subscription_history(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    "Get a user's subscription history (admin only)"
    return await get_subs_history(user_id, db)


@router.get("/history", response_model=SubscriptionHistory)
async def get_subscription_history(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    "Get current user's subscription history"
    return await get_subs_history(user.id, db)


@router.get("/", response_model=SubscriptionResponse)
async def get_subscription(
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    "Get current user's subscription details"
    return await get_subs(user.id, db)


@router.get("/{user_id}", response_model=SubscriptionResponse)
async def get_user_subscription(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    "Get a user's subscription details (admin only)"
    return await get_subs(user_id, db)


@router.put("/{user_id}", response_model=SubscriptionResponse)
async def update_user_subscription(
    user_id: int,
    data: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    "Update a user's subscription (admin only)"
    return await update_subs(user_id, data, db)


@router.put("/", response_model=SubscriptionResponse)
async def update_subscription(
    data: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    "Update current user's subscription"
    return await update_subs(user.id, data, db)


@router.delete("/{user_id}", response_model=SubscriptionResponse)
async def cancel_user_subscription(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    "Cancel a user's subscription (admin only)"
    return await cancel_subs(user_id, db)


@router.delete("/", response_model=SubscriptionResponse)
async def cancel_subscription(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    "Cancel current user's subscription"
    return await cancel_subs(user.id, db)
