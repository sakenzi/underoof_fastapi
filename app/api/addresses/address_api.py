from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.addresses.schemas.create import (
    CreateCity, 
    CreateStreet, 
    CreateLocation,
)
from app.api.addresses.schemas.response import (
    AddressResponse, 
    CitiesResponse, 
    StreetsResponse, 
    LocationsResponse,
)
from app.api.addresses.schemas.create import AddressSearchRequest
from app.api.addresses.commands.address_command import (
    bll_create_city, 
    bll_create_street, 
    bll_create_location,
    bll_get_all_cities, 
    bll_get_streets_by_city, 
    bll_get_locations_by_street,
    bll_get_locations, 
    bll_search_locations_by_address,
)
from database.db import get_db
from typing import List
import logging


logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/city",
    summary="Добавить город",
    response_model=AddressResponse
)
async def add_city(data: CreateCity, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating city: {data.city_name}")
    return await bll_create_city(data, db)


@router.post(
    "/street",
    summary="Добавить улицу",
    response_model=AddressResponse
)
async def add_street(data: CreateStreet, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating street: {data.street_name} in city {data.city_id}")
    return await bll_create_street(data, db)


@router.post(
    "/location",
    summary="Добавить адрес",
    response_model=AddressResponse
)
async def add_location(data: CreateLocation, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating location: {data.number} on street {data.street_id}")
    return await bll_create_location(data, db)


@router.get(
    "/cities",
    summary="Вывести все города",
    response_model=List[CitiesResponse]
)
async def all_cities(db: AsyncSession = Depends(get_db)):
    logger.info("Retrieving all cities")
    return await bll_get_all_cities(db)


@router.get(
    "/streets/{city_id}",
    summary="Вывести все улицы по ID города",
    response_model=List[StreetsResponse]
)
async def all_streets_by_city(city_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Retrieving streets for city {city_id}")
    return await bll_get_streets_by_city(city_id, db)


@router.get(
    "/locations/{street_id}",
    summary="Вывести все адреса по ID улицы",
    response_model=List[LocationsResponse]
)
async def all_locations_by_street(street_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Retrieving locations for street {street_id}")
    return await bll_get_locations_by_street(street_id, db)


@router.get(
    "/locations",
    summary="Вывести все локаций",
    response_model=List[LocationsResponse]
)
async def all_locations(db: AsyncSession = Depends(get_db)):
    logger.info(f"Retrieving locations")
    return await bll_get_locations(db)


@router.post(
    "/search",
    summary="Поиск локаций по адресу",
    response_model=List[LocationsResponse]
)
async def search_locations_by_address(search_request: AddressSearchRequest, db: AsyncSession = Depends(get_db)):
    return await bll_search_locations_by_address(query=search_request.query,db=db)