from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
from model.models import TypeAdvertisement
from sqlalchemy import select
from app.api.types.schemas.create import TypeCreate
from app.api.types.schemas.response import TypeResponse, TypeBase


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def create_type(type: TypeCreate, db: AsyncSession):
    stmt = await db.execute(select(TypeAdvertisement).filter(TypeAdvertisement.type_name==type.type_name))
    existing_type = stmt.scalar_one_or_none()

    if existing_type:
        raise HTTPException(
            status_code=400,
            detail="Такой тип обьявление уже существует"
        )
    
    new_type = TypeAdvertisement(
        type_name=type.type_name,
    )
    db.add(new_type)
    await db.commit()
    await db.refresh(new_type)
    return TypeResponse(message="Добавлено тип обьявление")


async def get_all_types(db: AsyncSession):
    stmt = await db.execute(select(TypeAdvertisement))
    types = stmt.scalars().all()

    if not types:
        return []
    
    return types