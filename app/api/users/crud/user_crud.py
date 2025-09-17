from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from model.models import User, UserRole, Logo, UserLogo
import logging


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