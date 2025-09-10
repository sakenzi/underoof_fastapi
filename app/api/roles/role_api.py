from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.roles.schemas.create import RoleCreate, UserRoleCreate
from app.api.roles.schemas.response import RoleResponse, RolesResponse
from app.api.roles.commands.role_command import bll_create_role, bll_get_all_roles, bll_assign_user_role
from database.db import get_db
from util.context_utils import get_access_token, validate_access_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/",
    summary="Создание ролей",
    response_model=RoleResponse
)
async def role_create(role: RoleCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating role: {role.role_name}")
    return await bll_create_role(role, db)

@router.get(
    "/",
    summary="Получить все роли",
    response_model=list[RolesResponse]
)
async def get_roles(db: AsyncSession = Depends(get_db)):
    logger.info("Retrieving all roles")
    return await bll_get_all_roles(db)

@router.post(
    "/assign",
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
        logger.error(f"Invalid user ID in token: {user_id_str}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")

    logger.info(f"Assigning role {data.role_id} to user {user_id}")
    return await bll_assign_user_role(user_id, data.role_id, db)