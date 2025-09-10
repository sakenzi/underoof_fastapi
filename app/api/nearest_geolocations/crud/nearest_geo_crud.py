from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from geoalchemy2.functions import ST_DWithin, ST_SetSRID, ST_MakePoint
from model.models import Advertisement, AdvertisementPhoto, Location, Street, City, UserRole, Role
import logging

logger = logging.getLogger(__name__)

async def dal_get_nearest_geolocations(latitude: float, longitude: float, radius: float, db: AsyncSession) -> list[Advertisement]:
    point = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
    
    stmt = select(Advertisement).join(Location, Advertisement.location_id == Location.id).where(
        Location.geom != None,
        ST_DWithin(Location.geom, point, radius)
    ).options(
        selectinload(Advertisement.advertisement_photos).selectinload(AdvertisementPhoto.photo),
        selectinload(Advertisement.location).selectinload(Location.street).selectinload(Street.city),
        selectinload(Advertisement.type_advertisement),
        selectinload(Advertisement.user_role).selectinload(UserRole.user),
        selectinload(Advertisement.user_role).selectinload(UserRole.role),
    )

    result = await db.execute(stmt)
    advertisements = result.scalars().all()
    logger.info(f"Retrieved {len(advertisements)} advertisements within {radius} degrees of ({latitude}, {longitude})")
    return advertisements