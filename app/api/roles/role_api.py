from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from database.db import get_db
import logging
from app.api.roles.commands.role_crud import create_role, get_all_roles
from app.api.roles.schemas.create import RoleCreate
from app.api.roles.schemas.response import RoleResponse, RolesResponse


router = APIRouter()

@router.post(
    '/create/role',
    summary="Создание ролей",
    response_model=RoleResponse
)
async def role_create(role: RoleCreate, db: AsyncSession = Depends(get_db)):
    return await create_role(role=role, db=db)


@router.get(
    "/roles",
    summary="Получить все роли",
    response_model=list[RolesResponse]
)
async def get_roles(db: AsyncSession = Depends(get_db)):
    roles = await get_all_roles(db=db)
    return roles