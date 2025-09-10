from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.types.schemas.create import TypeCreate
from app.api.types.schemas.response import TypeResponse, TypeBase
from app.api.types.commands.type_command import bll_create_type, bll_get_all_types
from database.db import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/",
    summary="Создание типа объявлений",
    response_model=TypeResponse
)
async def add_type(type_data: TypeCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating type: {type_data.type_name}")
    return await bll_create_type(type_data, db)

@router.get(
    "/",
    summary="Получить все типы объявлений",
    response_model=list[TypeBase]
)
async def all_types(db: AsyncSession = Depends(get_db)):
    logger.info("Retrieving all advertisement types")
    return await bll_get_all_types(db)