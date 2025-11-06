from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from model.models import (
    City, 
    Street, 
    Location,
)
import logging


logger = logging.getLogger(__name__)

async def dal_create_city(city_name: str, db: AsyncSession) -> City:
    existing_city = await dal_get_city_by_name(city_name, db)
    if existing_city:
        logger.info(f"City {city_name} already exists")
        return existing_city
    
    new_city = City(city_name=city_name)
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    logger.info(f"Created new city: {city_name}")
    return new_city


async def dal_get_city_by_name(city_name: str, db: AsyncSession) -> City | None:
    stmt = select(City).filter(City.city_name == city_name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def dal_get_city_by_id(city_id: int, db: AsyncSession) -> City | None:
    stmt = select(City).filter(City.id == city_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def dal_create_street(street_name: str, city_id: int, db: AsyncSession) -> Street:
    existing_street = await dal_get_street_by_name(street_name, city_id, db)
    if existing_street:
        logger.info(f"Street {street_name} already exists in city {city_id}")
        return existing_street
    
    new_street = Street(street_name=street_name, city_id=city_id)
    db.add(new_street)
    await db.commit()
    await db.refresh(new_street)
    logger.info(f"Created new street: {street_name} in city {city_id}")
    return new_street


async def dal_get_street_by_name(street_name: str, city_id: int, db: AsyncSession) -> Street | None:
    stmt = select(Street).filter(Street.street_name == street_name, Street.city_id == city_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def dal_get_street_by_id(street_id: int, db: AsyncSession) -> Street | None:
    stmt = select(Street).filter(Street.id == street_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def dal_create_location(number: str, latitude: float, longitude: float, street_id: int, db: AsyncSession) -> Location:
    existing_location = await dal_get_location_by_number(number, street_id, db)
    if existing_location:
        logger.info(f"Location {number} already exists on street {street_id}")
        return existing_location
    
    new_location = Location(number=number, latitude=latitude, longitude=longitude, street_id=street_id)
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    logger.info(f"Created new location: {number} on street {street_id}")
    return new_location


async def dal_get_location_by_number(number: str, street_id: int, db: AsyncSession) -> Location | None:
    stmt = select(Location).filter(Location.number == number, Location.street_id == street_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def dal_get_all_cities(db: AsyncSession) -> list[City]:
    stmt = select(City)
    result = await db.execute(stmt)
    cities = result.scalars().all()
    logger.info(f"Retrieved {len(cities)} cities")
    return cities


async def dal_get_streets_by_city(city_id: int, db: AsyncSession) -> list[Street]:
    stmt = select(Street).filter(Street.city_id == city_id)
    result = await db.execute(stmt)
    streets = result.scalars().all()
    logger.info(f"Retrieved {len(streets)} streets for city {city_id}")
    return streets


async def dal_get_locations_by_street(street_id: int, db: AsyncSession) -> list[Location]:
    stmt = select(Location).filter(Location.street_id == street_id)
    result = await db.execute(stmt)
    locations = result.scalars().all()
    logger.info(f"Retrieved {len(locations)} locations for street {street_id}")
    return locations


async def dal_get_locations(db: AsyncSession) -> list[Location]:
    stmt = select(Location)  
    result = await db.execute(stmt)
    locations = result.scalars().all()
    return locations


async def dal_search_locations_by_address(
    street_name: str,
    number: str, 
    db: AsyncSession
) -> list[Location]:
    stmt = select(Location).join(Street, Location.street_id == Street.id).join(City, Street.city_id == City.id)

    stmt = stmt.where(Street.street_name.ilike(f"%{street_name}%"))
    stmt = stmt.where(Location.number.ilike(f"%{number}%"))

    stmt = stmt.options(
        selectinload(Location.street).selectinload(Street.city)
    )

    result = await db.execute(stmt)
    locations = result.scalars().all()
    logger.info(f"Retrieved {len(locations)} locations matching address: street={street_name}, number={number}")
    return locations