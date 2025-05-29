from celery.schedules import crontab
from celery_worker import celery_app

celery_app.conf.beat_schedule = {
    "expire-subscriptions-every-5-min": {
        "task": "tasks.subscription_tasks.expire_old_subscriptions",
        "schedule": crontab(minute="*/5"),  # every 5 minutes
    }
}
