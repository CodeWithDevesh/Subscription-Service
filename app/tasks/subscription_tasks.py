from celery_worker import celery_app
from app.database import AsyncSessionLocal
from sqlalchemy.future import select
from app.models.subscription import Subscription, SubscriptionStatus
from datetime import datetime, timedelta, timezone
from app.models.plan import Plan

@celery_app.task
def expire_old_subscriptions():
    import asyncio
    asyncio.run(_expire_subs())

async def _expire_subs():
    async with AsyncSessionLocal() as db:
        now = datetime.now(timezone.utc)

        result = await db.execute(
            select(Subscription).join(Plan).where(Subscription.status == SubscriptionStatus.ACTIVE)
        )

        subs = result.scalars().all()

        for sub in subs:
            if sub.is_expired():
                sub.status = SubscriptionStatus.EXPIRED

        await db.commit()
