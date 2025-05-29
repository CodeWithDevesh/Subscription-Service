from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.timezone = "UTC"

from app.tasks.subscription_tasks import expire_old_subscriptions
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    "expire-subscriptions-every-5-mins": {
        "task": "tasks.subscription_tasks.expire_old_subscriptions",
        "schedule": 300.0,  # every 5 minutes (300 seconds)
    }
}