from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, HTTPException
from app.api.types.schemas.create import TypeCreate
from app.api.types.schemas.response import TypeResponse, TypeBase
from app.api.types.commands.type_crud import create_type, get_all_types
from database.db import get_db


router = APIRouter()

@router.post(
    '/create',
    summary="Создание типа обьявлений",
    response_model=TypeResponse
)
async def add_type(type: TypeCreate, db: AsyncSession = Depends(get_db)):
    return await create_type(type=type, db=db)


@router.get(
    '/types',
    summary="Получить все типы обьявление",
    response_model=list[TypeBase]
)
async def all_types(db: AsyncSession = Depends(get_db)):
    return await get_all_types(db=db)