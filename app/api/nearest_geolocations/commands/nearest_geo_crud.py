from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from geoalchemy2.functions import ST_DWithin, ST_SetSRID, ST_MakePoint
from model.models import User, Advertisement, AdvertisementPhoto, Location, Street, City, UserRole, Role
from fastapi import HTTPException


async def get_nearest_geolocations(latitude: float, longitude: float, radius: float, db: AsyncSession) -> list[Advertisement]:
    point = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
    
    stmt = await db.execute(
        select(Advertisement)
        .join(Location, Advertisement.location_id == Location.id)
        .where(
            Location.geom != None,
            ST_DWithin(Location.geom, point, radius)
        )
        .options(
            selectinload(Advertisement.advertisement_photos).selectinload(AdvertisementPhoto.photo),
            selectinload(Advertisement.location).selectinload(Location.street).selectinload(Street.city),
            selectinload(Advertisement.type_advertisement),
            selectinload(Advertisement.user_role).selectinload(UserRole.user),
            selectinload(Advertisement.user_role).selectinload(UserRole.role),
        )
    )

    results = stmt.scalars().all()
    for ad in results:
        ad.photo = [link.photo for link in ad.advertisement_photos]

    return results