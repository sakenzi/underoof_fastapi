from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.addresses.schemas.create import CreateCity, CreateStreet, CreateLocation
from app.api.addresses.schemas.response import AddressResponse, CitiesResponse, StreetsResponse, LocationsResponse
from app.api.addresses.crud.address_crud import (
    dal_create_city, dal_get_city_by_name, dal_get_city_by_id,
    dal_create_street, dal_get_street_by_name, dal_get_street_by_id,
    dal_create_location, dal_get_location_by_number,
    dal_get_all_cities, dal_get_streets_by_city, dal_get_locations_by_street
)
import logging
from typing import List


logger = logging.getLogger(__name__)

async def bll_create_city(data: CreateCity, db: AsyncSession) -> AddressResponse:
    existing_city = await dal_get_city_by_name(data.city_name, db)
    if existing_city:
        logger.error(f"Attempt to create duplicate city: {data.city_name}")
        raise HTTPException(status_code=400, detail="Такой город уже существует!")
    
    await dal_create_city(data.city_name, db)
    logger.info(f"City {data.city_name} created successfully")
    return AddressResponse(message="Город добавлен!")


async def bll_create_street(data: CreateStreet, db: AsyncSession) -> AddressResponse:
    city = await dal_get_city_by_id(data.city_id, db)
    if not city:
        logger.error(f"City ID {data.city_id} not found")
        raise HTTPException(status_code=404, detail="Город не найден")
    
    existing_street = await dal_get_street_by_name(data.street_name, data.city_id, db)
    if existing_street:
        logger.error(f"Attempt to create duplicate street: {data.street_name} in city {data.city_id}")
        raise HTTPException(status_code=400, detail="Такая улица уже существует!")
    
    await dal_create_street(data.street_name, data.city_id, db)
    logger.info(f"Street {data.street_name} created successfully in city {data.city_id}")
    return AddressResponse(message="Улица добавлена!")


async def bll_create_location(data: CreateLocation, db: AsyncSession) -> AddressResponse:
    street = await dal_get_street_by_id(data.street_id, db)
    if not street:
        logger.error(f"Street ID {data.street_id} not found")
        raise HTTPException(status_code=404, detail="Улица не найдена")
    
    existing_location = await dal_get_location_by_number(data.number, data.street_id, db)
    if existing_location:
        logger.error(f"Attempt to create duplicate location: {data.number} on street {data.street_id}")
        raise HTTPException(status_code=400, detail="Такой адрес уже существует")
    
    await dal_create_location(data.number, data.latitude, data.longitude, data.street_id, db)
    logger.info(f"Location {data.number} created successfully on street {data.street_id}")
    return AddressResponse(message="Адрес добавлен")


async def bll_get_all_cities(db: AsyncSession) -> List[CitiesResponse]:
    cities = await dal_get_all_cities(db)
    return [CitiesResponse(id=city.id, city_name=city.city_name) for city in cities]


async def bll_get_streets_by_city(city_id: int, db: AsyncSession) -> List[StreetsResponse]:
    city = await dal_get_city_by_id(city_id, db)
    if not city:
        logger.error(f"City ID {city_id} not found")
        raise HTTPException(status_code=404, detail="Город не найден")
    
    streets = await dal_get_streets_by_city(city_id, db)
    return [StreetsResponse(id=street.id, street_name=street.street_name) for street in streets]


async def bll_get_locations_by_street(street_id: int, db: AsyncSession) -> List[LocationsResponse]:
    street = await dal_get_street_by_id(street_id, db)
    if not street:
        logger.error(f"Street ID {street_id} not found")
        raise HTTPException(status_code=404, detail="Улица не найдена")
    
    locations = await dal_get_locations_by_street(street_id, db)
    return [LocationsResponse(id=location.id, number=location.number, latitude=location.latitude, longitude=location.longitude) for location in locations]