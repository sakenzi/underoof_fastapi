from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.roles.schemas.create import RoleCreate, UserRoleCreate
from app.api.roles.schemas.response import RoleResponse
from app.api.roles.crud.role_crud import (
    dal_create_role,
    dal_get_role_by_name,
    dal_get_all_roles,
    dal_get_role_by_id,
    dal_create_user_role
)
import logging


logger = logging.getLogger(__name__)

async def bll_create_role(role: RoleCreate, db: AsyncSession) -> RoleResponse:
    existing_role = await dal_get_role_by_name(role.role_name, db)
    if existing_role:
        logger.error(f"Attempt to create duplicate role: {role.role_name}")
        raise HTTPException(
            status_code=400,
            detail="Такой роль уже существует"
        )
    
    await dal_create_role(role.role_name, db)
    logger.info(f"Role {role.role_name} created successfully")
    return RoleResponse(message="Роль создана")


async def bll_get_all_roles(db: AsyncSession) -> list[dict]:
    roles = await dal_get_all_roles(db)
    return [{"id": role.id, "role_name": role.role_name} for role in roles]


async def bll_assign_user_role(user_id: int, role_id: int, db: AsyncSession) -> dict:
    role = await dal_get_role_by_id(role_id, db)
    if not role:
        logger.error(f"Role {role_id} not found")
        raise HTTPException(status_code=404, detail="Роль не найдена")

    user_role = await dal_create_user_role(user_id, role_id, db)
    logger.info(f"Role {role_id} assigned to user {user_id}")
    return {"message": "Роль успешно назначена"}