from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.api.addresses.commands.address_crud import create_city, create_street, create_location
from app.api.addresses.schemas.create import CreateCity, CreateStreet, CreateLocation
from database.db import get_db


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