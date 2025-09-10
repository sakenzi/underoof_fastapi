from app.api.advertisements.celery_tasks.celery_app import celery


if __name__ == "__main__":
    celery.start()