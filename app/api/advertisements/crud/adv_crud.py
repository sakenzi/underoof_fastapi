from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from model.models import Advertisement, AdvertisementPhoto, Photo, UserRole, Location, TypeAdvertisement, Street
from datetime import date
import logging
from typing import List, Tuple, Optional


logger = logging.getLogger(__name__)

async def dal_create_advertisement(
    description: str,
    number_of_room: int,
    quadrature: float,
    floor: int,
    price: int,
    from_the_date: date,
    before_the_date: date,
    location_id: int | None,
    type_advertisement_id: int,
    user_role_id: int,
    db: AsyncSession
) -> Advertisement:
    new_ad = Advertisement(
        description=description,
        number_of_room=number_of_room,
        quadrature=quadrature,
        floor=floor,
        price=price,
        from_the_date=from_the_date,
        before_the_date=before_the_date,
        location_id=location_id,
        type_advertisement_id=type_advertisement_id,
        user_role_id=user_role_id
    )
    db.add(new_ad)
    await db.commit()
    await db.refresh(new_ad)
    logger.info(f"Created advertisement ID {new_ad.id} for user_role_id {user_role_id}")
    return new_ad

async def dal_create_photo(advertisement_id: int, photo_link: str, db: AsyncSession) -> Photo:
    photo_obj = Photo(photo_link=photo_link)
    db.add(photo_obj)
    await db.flush()
    
    link = AdvertisementPhoto(advertisement_id=advertisement_id, photo_id=photo_obj.id)
    db.add(link)
    await db.commit()
    await db.refresh(photo_obj)
    logger.info(f"Created photo {photo_link} for advertisement ID {advertisement_id}")
    return photo_obj

async def dal_get_user_role(user_id: int, role_id: int, db: AsyncSession) -> UserRole | None:
    stmt = select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role_id)
    result = await db.execute(stmt)
    user_role = result.scalar_one_or_none()
    logger.info(f"Checked user_role for user_id {user_id}, role_id {role_id}: {'Found' if user_role else 'Not found'}")
    return user_role

async def dal_get_location_by_id(location_id: int, db: AsyncSession) -> Location | None:
    stmt = select(Location).where(Location.id == location_id)
    result = await db.execute(stmt)
    location = result.scalar_one_or_none()
    logger.info(f"Checked location_id {location_id}: {'Found' if location else 'Not found'}")
    return location

async def dal_get_type_advertisement_by_id(type_ad_id: int, db: AsyncSession) -> TypeAdvertisement | None:
    stmt = select(TypeAdvertisement).where(TypeAdvertisement.id == type_ad_id)
    result = await db.execute(stmt)
    type_ad = result.scalar_one_or_none()
    logger.info(f"Checked type_advertisement_id {type_ad_id}: {'Found' if type_ad else 'Not found'}")
    return type_ad

async def dal_get_advertisements_by_user(user_id: int, db: AsyncSession) -> List[Advertisement]:
    stmt = select(Advertisement).join(UserRole).where(UserRole.user_id == user_id).options(
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
    )
    result = await db.execute(stmt)
    advertisements = result.scalars().all()
    logger.info(f"Retrieved {len(advertisements)} advertisements for user_id {user_id}")
    return advertisements

async def dal_get_advertisements_by_role(role_id: int, db: AsyncSession) -> List[Advertisement]:
    stmt = select(Advertisement).join(UserRole).where(UserRole.role_id == role_id).options(
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
    )
    result = await db.execute(stmt)
    advertisements = result.scalars().all()
    logger.info(f"Retrieved {len(advertisements)} advertisements for role_id {role_id}")
    return advertisements

async def dal_get_advertisement_by_id(ad_id: int, db: AsyncSession) -> Advertisement | None:
    stmt = select(Advertisement).where(Advertisement.id == ad_id).options(
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
    )
    result = await db.execute(stmt)
    advertisement = result.scalars().first()
    logger.info(f"Retrieved advertisement ID {ad_id}: {'Found' if advertisement else 'Not found'}")
    return advertisement

async def dal_get_advertisements_by_filter(
    db: AsyncSession,
    type_advertisement_id: Optional[int] = None,
    location_id: Optional[int] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    city_id: Optional[int] = None,
    street_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0
) -> Tuple[List[Advertisement], int]:
    base_stmt = select(Advertisement).options(
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
    )

    conditions = []
    if type_advertisement_id:
        conditions.append(Advertisement.type_advertisement_id == type_advertisement_id)
    if location_id:
        conditions.append(Advertisement.location_id == location_id)
    if min_price:
        conditions.append(Advertisement.price >= min_price)
    if max_price:
        conditions.append(Advertisement.price <= max_price)
    if from_date and to_date:
        conditions.extend([
            Advertisement.from_the_date <= to_date,
            Advertisement.before_the_date >= from_date
        ])
    elif from_date:
        conditions.append(Advertisement.before_the_date >= from_date)
    elif to_date:
        conditions.append(Advertisement.from_the_date <= to_date)

    need_geo_join = city_id is not None or street_id is not None
    stmt = base_stmt
    if need_geo_join:
        stmt = stmt.join(Advertisement.location).join(Location.street)
        if city_id:
            conditions.append(Street.city_id == city_id)
        if street_id:
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
    advertisements = result.scalars().all()
    logger.info(f"Retrieved {len(advertisements)} advertisements with filters, total count: {total}")
    return advertisements, total