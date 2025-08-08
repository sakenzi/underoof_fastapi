from datetime import date
from sqlalchemy import update
from database.db import async_session_factory
from model.models import Advertisement
from app.api.advertisements.celery_tasks.celery_app import celery
import asyncio


@celery.task(name="app.tasks.deactivate_expired_ads")
def deactivate_expired_ads():
    asyncio.run(_deactivate_ads_async())


async def _deactivate_ads_async():
    async with async_session_factory() as session:
        stmt = (update(Advertisement)
            .where(Advertisement.before_the_date < date.today())
            .where(Advertisement.is_active == True)
            .values(is_active=False)    
        )
        await session.execute(stmt)
        await session.commit()
        print("[Celery Task] Объявления успешно деактивированы.")