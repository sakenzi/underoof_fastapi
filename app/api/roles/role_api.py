from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, HTTPException
from database.db import get_db
import logging
from app.api.roles.commands.role_crud import create_role, get_all_roles, create_user_role
from app.api.roles.schemas.create import RoleCreate, UserRoleCreate
from app.api.roles.schemas.response import RoleResponse, RolesResponse
from util.context_utils import get_access_token, validate_access_token


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


@router.post(
    "/assign/role",
    summary="Назначить роль пользователю",
)
async def assign_role(
    request: Request,
    data: UserRoleCreate,
    db: AsyncSession = Depends(get_db)
):
    access_token = await get_access_token(request)
    user_id_str = await validate_access_token(access_token)

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")

    return await create_user_role(db=db, user_id=user_id, role_id=data.role_id)