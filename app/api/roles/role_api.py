from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from database.db import get_db
import logging
from app.api.roles.commands.role_crud import create_role
from app.api.roles.schemas.create import RoleCreate
from app.api.roles.schemas.response import RoleResponse


router = APIRouter()

@router.post(
    '/create/role',
    summary="Создание ролей",
    response_model=RoleResponse
)
async def role_create(role: RoleCreate, db: AsyncSession = Depends(get_db)):
    return await create_role(role=role, db=db)