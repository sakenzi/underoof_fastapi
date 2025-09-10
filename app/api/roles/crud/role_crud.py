from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from model.models import Role, UserRole
import logging

logger = logging.getLogger(__name__)

async def dal_create_role(role_name: str, db: AsyncSession) -> Role:
    existing_role = await dal_get_role_by_name(role_name, db)
    if existing_role:
        logger.info(f"Role {role_name} already exists")
        return existing_role
    
    new_role = Role(role_name=role_name)
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    logger.info(f"Created new role: {role_name}")
    return new_role

async def dal_get_role_by_name(role_name: str, db: AsyncSession) -> Role | None:
    stmt = select(Role).filter(Role.role_name == role_name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def dal_get_all_roles(db: AsyncSession) -> list[Role]:
    stmt = select(Role)
    result = await db.execute(stmt)
    roles = result.scalars().unique().all()
    logger.info(f"Retrieved {len(roles)} roles")
    return roles

async def dal_get_role_by_id(role_id: int, db: AsyncSession) -> Role | None:
    stmt = select(Role).where(Role.id == role_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def dal_create_user_role(user_id: int, role_id: int, db: AsyncSession) -> UserRole:
    existing_user_role = await dal_get_user_role(user_id, role_id, db)
    if existing_user_role:
        logger.info(f"Role {role_id} already assigned to user {user_id}")
        return existing_user_role
    
    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    await db.commit()
    await db.refresh(user_role)
    logger.info(f"Assigned role {role_id} to user {user_id}")
    return user_role

async def dal_get_user_role(user_id: int, role_id: int, db: AsyncSession) -> UserRole | None:
    stmt = select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()