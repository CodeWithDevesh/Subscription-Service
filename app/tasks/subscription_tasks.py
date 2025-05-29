from celery_worker import celery_app
from app.database import SyncSessionLocal
from sqlalchemy.future import select
from app.models.subscription import Subscription, SubscriptionStatus
from datetime import datetime, timezone
from app.models.plan import Plan


@celery_app.task(name="tasks.subscription_tasks.expire_old_subscriptions")
def expire_old_subscriptions():
    _expire_subs()


def _expire_subs():
    with SyncSessionLocal() as db:
        now = datetime.now(timezone.utc)

        result = db.execute(
            select(Subscription)
            .join(Plan)
            .where(Subscription.status == SubscriptionStatus.ACTIVE)
        )

        subs = result.scalars().all()

        for sub in subs:
            if sub.is_expired:
                sub.status = SubscriptionStatus.EXPIRED

        db.commit()
