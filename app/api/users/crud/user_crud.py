from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from model.models import User, UserRole, Logo, UserLogo
import logging
from app.api.users.schemas.update import UserUpdate
from typing import Optional


logger = logging.getLogger(__name__)

async def dal_get_user_by_id(user_id: int, db: AsyncSession) -> User | None:
    result = await db.execute(
        select(User)
        .options(
            joinedload(User.user_roles).joinedload(UserRole.role),
            joinedload(User.user_logos).joinedload(UserLogo.logo)
        )
        .filter(User.id == user_id)
    )
    user = result.unique().scalar_one_or_none()
    if user:
        logger.info(f"Retrieved user data for user_id: {user_id}")
    else:
        logger.warning(f"No user found for user_id: {user_id}")
    return user


async def dal_create_logo(user_id: int, logo_link: str, db: AsyncSession) -> Logo:
    logo_obj = Logo(logo_link=logo_link)
    db.add(logo_obj)
    await db.flush()

    user_logo = UserLogo(user_id=user_id, logo_id=logo_obj.id)
    db.add(user_logo)
    await db.commit()
    await db.refresh(logo_obj)
    return logo_obj


async def dal_update_user(
    user_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    surname: Optional[str] = None,
    phone_number: Optional[str] = None,
    db: AsyncSession = None
) -> User | None:
    user = await dal_get_user_by_id(user_id, db)
    if not user:
        logger.warning(f"No user found for user_id: {user_id} to update")
        return None

    updates = {}
    if first_name is not None:
        updates["first_name"] = first_name
    if last_name is not None:
        updates["last_name"] = last_name
    if surname is not None:
        updates["surname"] = surname
    if phone_number is not None:
        updates["phone_number"] = phone_number

    if updates:
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(**updates)
        )
        await db.commit()
        await db.refresh(user)
        logger.info(f"Updated user data for user_id: {user_id}, updated fields: {list(updates.keys())}")
    else:
        logger.info(f"No fields to update for user_id: {user_id}")

    return user