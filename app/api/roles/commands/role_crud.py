from sqlalchemy.ext.asyncio import AsyncSession
import logging
from fastapi import HTTPException
from model.models import Role
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