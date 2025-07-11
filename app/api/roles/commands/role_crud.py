from sqlalchemy.ext.asyncio import AsyncSession
import logging
from fastapi import HTTPException
from model.models import Role, User, UserRole
from app.api.roles.schemas.create import RoleCreate
from app.api.roles.schemas.response import RoleResponse
from sqlalchemy import select, update


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def create_role(role: RoleCreate, db: AsyncSession):
    stmt = await db.execute(select(Role).filter(Role.role_name == role.role_name))
    existing_role = stmt.scalar_one_or_none()

    if existing_role:
        raise HTTPException(
            status_code=400,
            detail="Такой роль уже существует"
        )
    
    new_role = Role(
        role_name=role.role_name,
    )
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return RoleResponse(
        message="Роль создан"
    )


async def get_all_roles(db: AsyncSession):
    stmt = await db.execute(select(Role))
    roles = stmt.scalars().unique().all()

    if not roles:
        return []
    
    return roles


async def create_user_role(user_id: int, role_id: int, db: AsyncSession):
    stmt = 