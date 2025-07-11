from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.api.addresses.schemas.create import CreateCity, CreateLocation, CreateStreet
from model.models import City, Street, Location
from sqlalchemy import select
import logging


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
    