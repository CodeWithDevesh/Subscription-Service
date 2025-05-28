from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.auth.dependencies import get_current_user, get_current_admin
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.plan import Plan
from app.models.user import User
from app.schemas.subscription_schema import SubscriptionCreate
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.post("/")
async def create_subscription(
    data: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    existing = await db.execute(select(Subscription).where(Subscription.user_id == user.id))
    if existing.scalar():
        raise HTTPException(status_code=400, detail="User already has a subscription")

    # Check if plan exists
    plan_result = await db.execute(select(Plan).where(Plan.id == data.plan_id))
    plan = plan_result.scalar()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    now = datetime.now(timezone.utc)

    sub = Subscription(
        user_id=user.id,
        plan_id=plan.id,
        start_date=now,
        status=SubscriptionStatus.ACTIVE
    )

    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    return {"message": "Subscribed successfully!", "plan": plan.name}


@router.get("/{user_id}")
async def get_user_subscription(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin)
):
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == user_id)
    )
    sub = result.scalar()
    if not sub:
        raise HTTPException(status_code=404, detail="No subscription found")
    return sub


@router.put("/{user_id}")
async def update_user_subscription(
    user_id: int,
    data: SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin)
):
    # Get existing subscription
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == user_id)
    )
    sub = result.scalar()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    # Fetch new plan
    plan_result = await db.execute(select(Plan).where(Plan.id == data.plan_id))
    plan = plan_result.scalar()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # Update fields
    now = datetime.now(timezone.utc)
    sub.plan_id = plan.id
    sub.start_date = now
    sub.end_date = now + timedelta(days=plan.duration_days)
    sub.status = SubscriptionStatus.ACTIVE

    await db.commit()
    await db.refresh(sub)
    return {"message": "Subscription updated", "plan": plan.name}


@router.delete("/{user_id}")
async def cancel_subscription(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin)
):
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == user_id)
    )
    sub = result.scalar()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    await db.delete(sub)
    await db.commit()
    return {"message": "Subscription cancelled"}
