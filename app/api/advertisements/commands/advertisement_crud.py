from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
from sqlalchemy import select, func, distinct
from model.models import (Advertisement, AdvertisementPhoto, TypeAdvertisement, Photo, UserRole,
                          Location, Street, City, User)
from sqlalchemy.orm import joinedload, selectinload
from app.api.advertisements.schemas.create import CreateAdvertisementByLessee, CreateAdvertisementBySeller
from app.api.advertisements.schemas.response import AdvertisementsResponse, AdvertisementResponse
import uuid
import shutil
import os
from typing import Optional, List, Tuple
from datetime import date


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


async def get_advertisement_by_user(user_id: int, db: AsyncSession) -> list[AdvertisementsResponse]:
    stmt = await db.execute(select(Advertisement).join(UserRole).where(UserRole.user_id == user_id).options(
        selectinload(Advertisement.location)
            .selectinload(Location.street)
            .selectinload(Street.city),
        selectinload(Advertisement.type_advertisement),
        selectinload(Advertisement.user_role)
            .selectinload(UserRole.user),
        selectinload(Advertisement.user_role)
            .selectinload(UserRole.role),
        selectinload(Advertisement.advertisement_photos)
            .selectinload(AdvertisementPhoto.photo)
    ))
    advertisements = stmt.scalars().all()

    for ad in advertisements:
        ad.photo = [link.photo for link in ad.advertisement_photos]

    return advertisements


async def get_advertisements_by_user(user_id: int, db: AsyncSession) -> list[Advertisement]:
    stmt = await db.execute(select(Advertisement).join(UserRole).where(UserRole.user_id == user_id).options(
        selectinload(Advertisement.advertisement_photos)
            .selectinload(AdvertisementPhoto.photo)
    ))
    advertisements = stmt.scalars().all()

    for ad in advertisements:
        ad.photo = [link.photo for link in ad.advertisement_photos]

    return advertisements


async def get_all_seller_advertisements_for_lessee(user_id: int, db: AsyncSession) -> list[Advertisement]:
    stmt = await db.execute(select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == 1))
    role = stmt.scalar_one_or_none()

    if not role:
        raise HTTPException(status_code=403, detail="Доступ разрешён только арендаторам (role_id=1)")
    
    ads_stmt = await db.execute(select(Advertisement).join(UserRole).where(
        UserRole.role_id == 2
    ).options(
        selectinload(Advertisement.advertisement_photos)
            .selectinload(AdvertisementPhoto.photo)
    ))
    
    result = ads_stmt.scalars().all()

    for ad in result:
        ad.photo = [link.photo for link in ad.advertisement_photos]

    return result


async def get_all_lessee_advertisements_for_seller(user_id: int, db: AsyncSession) -> list[Advertisement]:
    stmt = await db.execute(select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == 2))
    role = stmt.scalar_one_or_none()

    if not role:
        raise HTTPException(status_code=403, detail="Доступ разрешен только продовцам (role_id=2)")
    
    ads_stmt = await db.execute(select(Advertisement).join(UserRole).where(
        UserRole.role_id == 1
    ).options(
        selectinload(Advertisement.advertisement_photos)
            .selectinload(AdvertisementPhoto.photo)
    ))

    result = ads_stmt.scalars().all()

    for ad in result:
        ad.photo = [link.photo for link in ad.advertisement_photos]

    return result


async def get_advertisement_by_id(ad_id: int, db: AsyncSession) -> Advertisement:
    stmt = await db.execute(select(Advertisement).where(Advertisement.id == ad_id).options(
        selectinload(Advertisement.advertisement_photos)
            .selectinload(AdvertisementPhoto.photo),
        selectinload(Advertisement.location)
            .selectinload(Location.street)
            .selectinload(Street.city),
        selectinload(Advertisement.type_advertisement),
        selectinload(Advertisement.user_role)
            .selectinload(UserRole.user),
        selectinload(Advertisement.user_role)
            .selectinload(UserRole.role)
    ))

    result = stmt.scalars().first()

    if not result:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    result.photo = [link.photo for link in result.advertisement_photos]

    return result


async def get_advertisements_by_filter(
    db: AsyncSession,
    *,
    type_advertisement_id: Optional[int] = None,
    location_id: Optional[int] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    city_id: Optional[int] = None,
    street_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
) -> Tuple[List[Advertisement], int]:
    base_stmt = (
        select(Advertisement)
        .options(
            selectinload(Advertisement.advertisement_photos).selectinload(AdvertisementPhoto.photo),
            selectinload(Advertisement.location).selectinload(Location.street).selectinload(Street.city),
            selectinload(Advertisement.user_role).selectinload(UserRole.user),
            selectinload(Advertisement.user_role).selectinload(UserRole.role),
            selectinload(Advertisement.type_advertisement),
        )
    )

    conditions = []

    if type_advertisement_id is not None:
        conditions.append(Advertisement.type_advertisement_id == type_advertisement_id)
    if location_id is not None:
        conditions.append(Advertisement.location_id == location_id)
    if min_price is not None:
        conditions.append(Advertisement.price >= min_price)
    if max_price is not None:
        conditions.append(Advertisement.price <= max_price)

    if from_date and to_date:
        conditions += [
            Advertisement.from_the_date <= to_date,
            Advertisement.before_the_date >= from_date,
        ]
    elif from_date:
        conditions.append(Advertisement.before_the_date >= from_date)
    elif to_date:
        conditions.append(Advertisement.from_the_date <= to_date)

    need_geo_join = city_id is not None or street_id is not None
    stmt = base_stmt
    if need_geo_join:
        stmt = stmt.join(Advertisement.location)
        stmt = stmt.join(Location.street)
        if city_id is not None:
            conditions.append(Street.city_id == city_id)
        if street_id is not None:
            conditions.append(Street.id == street_id)

    if conditions:
        stmt = stmt.where(*conditions)

    count_stmt = select(func.count(distinct(Advertisement.id)))
    if need_geo_join:
        count_stmt = count_stmt.join(Advertisement.location).join(Location.street)
    if conditions:
        count_stmt = count_stmt.where(*conditions)

    total = (await db.execute(count_stmt)).scalar_one()

    stmt = stmt.offset(offset).limit(limit)
    result = await db.execute(stmt)
    items: List[Advertisement] = result.scalars().all()

    for ad in items:
        ad.photo = [link.photo for link in ad.advertisement_photos]

    return items, total