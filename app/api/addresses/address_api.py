from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.api.addresses.commands.address_crud import (create_city, create_street, create_location,
                                                     get_all_cities, get_streets_by_city, get_locations_by_street)
from app.api.addresses.schemas.create import CreateCity, CreateStreet, CreateLocation
from app.api.addresses.schemas.response import CitiesResponse, StreetsResponse, LocationsResponse
from database.db import get_db
from typing import List


router = APIRouter()

@router.post(
    '/create/city',
    summary='Добавить город'
)
async def add_city(data: CreateCity, db: AsyncSession = Depends(get_db)):
    return await create_city(data=data, db=db)


@router.post(
    '/create/street',
    summary='Добавить улийцу'
)
async def add_street(data: CreateStreet, db: AsyncSession = Depends(get_db)):
    return await create_street(data=data, db=db)


@router.post(
    '/create/location',
    summary="Добавить адрес"
)
async def add_location(data: CreateLocation, db: AsyncSession = Depends(get_db)):
    return await create_location(data=data, db=db)


@router.get(
    '/all/cities',
    summary='Выводить все города',
    response_model=List[CitiesResponse]
)
async def all_cities(db: AsyncSession = Depends(get_db)):
    return await get_all_cities(db=db)


@router.get(
    '/all/streets/{city_id}',
    summary="Выводить все улицы по id города",
    response_model=List[StreetsResponse]
)
async def all_streets_by_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await get_streets_by_city(city_id, db)


@router.get(
    '/all/locations/{street_id}',
    summary="Выводить все локаций по id улицы",
    response_model=List[LocationsResponse]
)
async def all_locations_by_street(street_id: int, db: AsyncSession = Depends(get_db)):
    return await get_locations_by_street(street_id, db)