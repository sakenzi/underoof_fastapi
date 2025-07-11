from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.api.addresses.commands.address_crud import create_city
from app.api.addresses.schemas.create import CreateCity
from database.db import get_db


router = APIRouter()

@router.post(
    '/create/city',
    summary='Добавить город'
)
async def add_city(data: CreateCity, db: AsyncSession = Depends(get_db)):
    return await create_city(data=data, db=db)