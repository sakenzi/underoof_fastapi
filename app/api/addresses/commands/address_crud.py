from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.api.addresses.schemas.create import CreateCity, CreateLocation, CreateStreet
from app.api.addresses.schemas.response import CitiesResponse, StreetsResponse
from model.models import City, Street, Location
from sqlalchemy import select
import logging
from typing import List


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def create_city(data: CreateCity, db: AsyncSession):
    stmt = await db.execute(select(City).filter(City.city_name == data.city_name))
    city = stmt.scalar_one_or_none()

    if city:
        raise HTTPException(
            status_code=400,
            detail="Такой город уже существует!"
        )
    
    new_city = City(
        city_name=data.city_name,
    )
    db.add(new_city)
    await db.commit()
    await db.refresh(new_city)
    return {"message": "Город добавлен!"}


async def create_street(data: CreateStreet, db: AsyncSession):
    stmt = await db.execute(select(Street).filter(Street.street_name == data.street_name))
    street = stmt.scalar_one_or_none()

    if street:
        raise HTTPException(
            status_code=400,
            detail="Такая улица уже существует!"
        )
    
    new_street = Street(
        street_name=data.street_name,
        city_id=data.city_id,
    )
    db.add(new_street)
    await db.commit()
    await db.refresh(new_street)
    return {"message": "Улица добавлено!"}


async def create_location(data: CreateLocation, db: AsyncSession):
    stmt = await db.execute(select(Location).filter(Location.number == data.number))
    location = stmt.scalar_one_or_none()

    if location:
        raise HTTPException(
            status_code=400,
            detail="Такой адрес существует"
        )
    
    new_location = Location(
        number=data.number,
        latitude=data.latitude,
        longitude=data.longitude,
        street_id=data.street_id,
    )
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    return {"message": "Адрес добавлен"}
    

async def get_all_cities(db: AsyncSession):
    stmt = await db.execute(select(City))
    all_cities = stmt.scalars().all()
    if not all_cities:
        raise HTTPException(
            status_code=404,
            detail="Город не найден!"
        )
    return [CitiesResponse.from_orm(cities) for cities in all_cities]


async def get_streets_by_city(city_id: int, db: AsyncSession) -> List[StreetsResponse]:
    stmt = await db.execute(select(City).filter(City.id==city_id))
    city = stmt.scalars().first()
    if not city:
        raise HTTPException(
            status_code=404,
            detail="Город не найден"
        )
    street_result = await db.execute(select(Street).filter(Street.city_id==city.id))
    streets =street_result.scalars().all()

    return [StreetsResponse.from_orm(street) for street in streets]