from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.subscription import Subscription, SubscriptionStatus
from app.schemas.subscription_schema import (
    SubscriptionCreate,
    SubscriptionDetail,
    SubscriptionResponse,
    SubscriptionHistory,
)
from app.models.user import User
from app.models.plan import Plan
from datetime import datetime, timedelta, timezone


async def create_subs(
    user_id: int,
    data: SubscriptionCreate,
    db: AsyncSession,
):
    # Check if user already has an active subscription
    existing = await db.execute(
        select(Subscription).where(
            Subscription.user_id == user_id,
            Subscription.status == SubscriptionStatus.ACTIVE,
        )
    )
    if existing.scalar():
        raise HTTPException(
            status_code=400,
            detail="User already has an active subscription, cancel it first",
        )

    # Check if plan exists
    plan_result = await db.execute(select(Plan).where(Plan.id == data.plan_id))
    plan = plan_result.scalar()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    now = datetime.now(timezone.utc)
    end = now + timedelta(days=plan.duration_days)

    sub = Subscription(
        user_id=user_id,
        plan_id=plan.id,
        start_date=now,
        end_date=end,
        status=SubscriptionStatus.ACTIVE,
    )

    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    return SubscriptionResponse(
        ok=True, message="Subscription created successfully", data=sub
    )


async def get_subs(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == user_id,
            Subscription.status == SubscriptionStatus.ACTIVE,
        )
    )
    subs = result.scalar()
    if not subs:
        raise HTTPException(status_code=404, detail="No active subscription found")
    return SubscriptionDetail(
        ok=True, message="Subscription retrieved successfully", data=subs
    )


async def get_subs_history(
    user_id: int,
    db: AsyncSession,
):
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == user_id)
    )
    subs = result.scalars().all()
    if not subs:
        raise HTTPException(status_code=404, detail="No subscription history found")
    return SubscriptionHistory(
        ok=True, message="Subscription history retrieved successfully", data=subs
    )


async def update_subs(
    user_id: int,
    data: SubscriptionCreate,
    db: AsyncSession,
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
    return SubscriptionResponse(
        ok=True, message="Subscription updated successfully", data=sub
    )


async def cancel_subs(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == user_id,
            Subscription.status == SubscriptionStatus.ACTIVE,
        )
    )
    sub = result.scalar()
    if not sub:
        raise HTTPException(status_code=404, detail="No active Subscription found")

    # Update subscription status to CANCELLED
    sub.status = SubscriptionStatus.CANCELLED
    sub.end_date = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(sub)
    return SubscriptionResponse(
        ok=True, message="Subscription cancelled successfully", data=sub
    )


async def get_active_subs(db: AsyncSession):
    result = await db.execute(
        select(Subscription).where(
            Subscription.status == SubscriptionStatus.ACTIVE
        )
    )
    subs = result.scalars().all()
    if not subs:
        raise HTTPException(status_code=404, detail="No active subscriptions found")
    return SubscriptionHistory(
        ok=True, message="Active subscriptions retrieved successfully", data=subs
    )