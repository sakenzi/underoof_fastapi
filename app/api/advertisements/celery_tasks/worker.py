from app.api.advertisements.celery_tasks.celery_app import celery
import app.api.advertisements.celery_tasks.tasks


if __name__ == "__main__":
    celery.start()