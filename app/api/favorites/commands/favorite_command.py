from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.favorites.crud.favorite_crud import dal_create_favorite, dal_get_favorites_by_user, dal_get_favorite_by_id, dal_delete_favorite
from app.api.advertisements.schemas.response import AdvertisementListResponse
from app.api.advertisements.commands.adv_command import _format_advertisements_response
from app.api.favorites.schemas.response import FavoriteListResponse, FavoriteResponse
from model.models import Advertisement
import logging
from typing import List


logger = logging.getLogger(__name__)

async def bll_create_favorite(user_id: int, advertisement_id: int, db: AsyncSession) -> dict:
    advertisement = await db.get(Advertisement, advertisement_id)
    if not advertisement:
        logger.error(f"Advertisement ID {advertisement_id} not found")
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    existing_favorite = await dal_get_favorite_by_id(advertisement_id, user_id, db)
    if existing_favorite:
        logger.warning(f"Favorite already exists for user_id={user_id}, advertisement_id={advertisement_id}")
        raise HTTPException(status_code=400, detail="Объявление уже в избранном")
    
    favorite = await dal_create_favorite(user_id, advertisement_id, db)
    return {
        "id": favorite.id,
        "user_id": user_id,
        "advertisement_id": advertisement_id,
        "message": "Объявление добавлено в избранное"
    }


async def bll_get_favorites_by_user(user_id: int, db: AsyncSession) -> List[FavoriteListResponse]:
    favorites = await dal_get_favorites_by_user(user_id, db)
    if not favorites:
        logger.info(f"No favorites found for user_id={user_id}")
        return []

    results = []
    advertisements = [favorite.advertisement for favorite in favorites]
    formatted_ads = await _format_advertisements_response(advertisements, logger)

    for favorite, formatted_ad in zip(favorites, formatted_ads):
        results.append(FavoriteListResponse(
            favorite_id=favorite.id,
            advertisement=formatted_ad
        ))

    logger.info(f"Formatted {len(results)} favorites for user_id={user_id}")
    return results


async def bll_delete_favorite(favorite_id: int, user_id: int, db: AsyncSession) -> dict:
    success = await dal_delete_favorite(favorite_id, user_id, db)
    if not success:
        logger.error(f"Failed to delete favorite {favorite_id} for user_id={user_id}")
        raise HTTPException(status_code=404, detail="Избранное не найдено")
    return {"message": "Объявление удалено из избранного"}