from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
from sqlalchemy import select
from model.models import Advertisement, AdvertisementPhoto, TypeAdvertisement, Photo, UserRole
from sqlalchemy.orm import joinedload, selectinload
from app.api.advertisements.schemas.create import CreateAdvertisementByLessee, CreateAdvertisementBySeller
import uuid
import shutil
import os


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

UPLOAD_FOLDER = "uploads/photo_advertisements"

async def create_advertisement_by_lessee(user_id: int, data: CreateAdvertisementByLessee, db: AsyncSession):
    stmt = await db.execute(select(UserRole).where(UserRole.user_id==user_id, UserRole.role_id==1))
    user_role = stmt.scalar_one_or_none()

    if not user_role:
        raise HTTPException(
            status_code=403,
            detail="Доступ запрещен"
        )
    
    new_ad = Advertisement(
        description=data.description,
        number_of_room=data.number_of_room,
        quadrature=data.quadrature,
        floor=data.floor,
        location_id=data.location_id,
        type_advertisement_id=data.type_advertisement_id,
        price=data.price,
        from_the_date=data.from_the_date,
        before_the_date=data.before_the_date,
        user_role_id=user_role.id
    )

    db.add(new_ad)
    await db.commit()
    await db.refresh(new_ad)

    return {"message": "Объявление успешно создано"}


async def create_advertisement_by_seller(user_id: int, data: dict, db: AsyncSession):
    stmt = await db.execute(select(UserRole).where(UserRole.user_id==user_id, UserRole.role_id==2))
    user_role = stmt.scalar_one_or_none()

    if not user_role:
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    new_ad = Advertisement(
        description=data["description"],
        number_of_room=data["number_of_room"],
        quadrature=data["quadrature"],
        floor=data["floor"],
        price=data["price"],
        from_the_date=data["from_the_date"],
        before_the_date=data["before_the_date"],
        location_id=data["location_id"],
        type_advertisement_id=data["type_advertisement_id"],
        user_role_id=user_role.id
    )
    db.add(new_ad)
    await db.flush()

    for photo in data["photos"]:
        filename = f"{uuid.uuid4()}.{photo.filename.split('.')[-1]}"
        save_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        photo_obj = Photo(photo_link=save_path)
        db.add(photo_obj)
        await db.flush()

        link = AdvertisementPhoto(
            photo_id=photo_obj.id,
            advertisement_id=new_ad.id
        )
        db.add(link)

    await db.commit()
    await db.refresh(new_ad)

    return {"message": "Объявление с фото создано", "ad_id": new_ad.id}


async def get_advertisements_by_lessee(user_id: int, db: AsyncSession) -> list[Advertisement]:
    query = await db.execute(select(Advertisement).where(Advertisement.user_role_id))