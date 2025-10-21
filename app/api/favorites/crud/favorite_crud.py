from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from model.models import Favorite, Advertisement, AdvertisementPhoto, Street, Location, UserRole, User, UserLogo
from typing import List, Optional
import logging
from sqlalchemy.orm import selectinload
from fastapi import HTTPException


logger = logging.getLogger(__name__)

async def dal_create_favorite(user_id: int, advertisement_id: int, db: AsyncSession) -> Favorite:
    favorite = Favorite(user_id=user_id, advertisement_id=advertisement_id)
    db.add(favorite)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        logger.warning(f"Duplicate favorite attempted for user_id={user_id}, advertisement_id={advertisement_id}")
        raise HTTPException(status_code=400, detail="Объявление уже в избранном")
    await db.refresh(favorite)
    logger.info(f"Favorite created for user_id={user_id}, advertisement_id={advertisement_id}")
    return favorite


async def dal_get_favorites_by_user(user_id: int, db: AsyncSession) -> List[Favorite]:
    stmt = select(Favorite).where(Favorite.user_id == user_id).options(
        selectinload(Favorite.advertisement).selectinload(Advertisement.advertisement_photos).selectinload(AdvertisementPhoto.photo),
        selectinload(Favorite.advertisement).selectinload(Advertisement.location).selectinload(Location.street).selectinload(Street.city),
        selectinload(Favorite.advertisement).selectinload(Advertisement.type_advertisement),
        selectinload(Favorite.advertisement).selectinload(Advertisement.user_role).selectinload(UserRole.user).selectinload(User.user_logos).selectinload(UserLogo.logo),
        selectinload(Favorite.advertisement).selectinload(Advertisement.user_role).selectinload(UserRole.role),
        selectinload(Favorite.advertisement).selectinload(Advertisement.favorites)
    )
    result = await db.execute(stmt)
    favorites = result.scalars().all()
    logger.info(f"Получено {len(favorites)} избранных для user_id={user_id}")
    return favorites


async def dal_get_favorite_by_id(favorite_id: int, user_id: int, db: AsyncSession) -> Optional[Favorite]:
    stmt = select(Favorite).where(
        Favorite.advertisement_id == favorite_id,  
        Favorite.user_id == user_id
    )
    result = await db.execute(stmt)
    favorite = result.scalar_one_or_none()
    if favorite:
        logger.info(f"Favorite found for user_id={user_id}, advertisement_id={favorite_id}")
    else:
        logger.warning(f"Favorite not found for user_id={user_id}, advertisement_id={favorite_id}")
    return favorite


async def dal_delete_favorite(favorite_id: int, user_id: int, db: AsyncSession) -> bool:
    stmt = delete(Favorite).where(Favorite.id == favorite_id, Favorite.user_id == user_id)
    result = await db.execute(stmt)
    if result.rowcount > 0:
        await db.commit()
        logger.info(f"Favorite {favorite_id} deleted for user_id={user_id}")
        return True
    logger.warning(f"Favorite {favorite_id} not found for deletion by user_id={user_id}")
    return False