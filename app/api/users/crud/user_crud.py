from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from model.models import User, UserRole
import logging


logger = logging.getLogger(__name__)

async def dal_get_user_by_id(user_id: int, db: AsyncSession) -> User | None:
    result = await db.execute(
        select(User)
        .options(
            joinedload(User.user_roles).joinedload(UserRole.role)
        )
        .filter(User.id == user_id)
    )
    user = result.unique().scalar_one_or_none()
    if user:
        logger.info(f"Retrieved user data for user_id: {user_id}")
    else:
        logger.warning(f"No user found for user_id: {user_id}")
    return user