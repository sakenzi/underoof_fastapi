from celery import Celery
from celery.schedules import crontab


celery = Celery(
    "advertisement_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

celery.conf.timezone = 'Asia/Almaty'
celery.conf.enable_utc = False

celery.conf.beat_shedule = {
    'deactivate-expired-ads-every-night': {
        'task': 'app.tasks.deactivate_expired_ads',
        'shedule': crontab(hour=0, minute=0),
    }
}

