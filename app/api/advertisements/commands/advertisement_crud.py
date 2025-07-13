from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
from sqlalchemy import select
from model.models import Advertisement, AdvertisementPhoto, TypeAdvertisement, Photo, UserRole
from sqlalchemy.orm import joinedload, selectinload
from app.api.advertisements.schemas.create import CreateAdvertisementByLessee


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def create_advertisement_by_lessee(role_id: int, data: CreateAdvertisementByLessee, db: AsyncSession):
    stmt = await db.execute(select())