from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.types.schemas.create import TypeCreate
from app.api.types.schemas.response import TypeResponse, TypeBase
from app.api.types.crud.type_crud import dal_create_type, dal_get_type_by_name, dal_get_all_types
import logging

logger = logging.getLogger(__name__)

async def bll_create_type(type_data: TypeCreate, db: AsyncSession) -> TypeResponse:
    existing_type = await dal_get_type_by_name(type_data.type_name, db)
    if existing_type:
        logger.error(f"Attempt to create duplicate type: {type_data.type_name}")
        raise HTTPException(
            status_code=400,
            detail="Такой тип объявления уже существует"
        )
    
    await dal_create_type(type_data.type_name, db)
    logger.info(f"Type {type_data.type_name} created successfully")
    return TypeResponse(message="Добавлено тип объявления")

async def bll_get_all_types(db: AsyncSession) -> list[TypeBase]:
    types = await dal_get_all_types(db)
    return [TypeBase(id=type_.id, type_name=type_.type_name) for type_ in types]