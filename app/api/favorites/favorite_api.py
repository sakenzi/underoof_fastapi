from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.favorites.commands.favorite_command import bll_create_favorite, bll_get_favorites_by_user, bll_delete_favorite
from app.api.advertisements.schemas.response import AdvertisementListResponse
from database.db import get_db
from util.context_utils import get_access_token, validate_access_token
from app.api.favorites.schemas.create import FavoriteCreate
from app.api.favorites.schemas.response import FavoriteListResponse, FavoriteResponse
import logging
from typing import List


logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "",
    summary="Добавить объявление в избранное",
    response_model=FavoriteResponse
)
async def add_favorite(
    data: FavoriteCreate,
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_db)
):
    user_id_str = await validate_access_token(access_token)
    try:
        user_id = int(user_id_str)
    except ValueError:
        logger.error(f"Invalid user ID in token: {user_id_str}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"User {user_id} adding favorite for advertisement {data.advertisement_id}")
    return await bll_create_favorite(user_id, data.advertisement_id, db)

@router.get(
    "",
    summary="Получить избранные объявления пользователя",
    response_model=List[FavoriteListResponse]
)
async def get_favorites(
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_db)
):
    user_id_str = await validate_access_token(access_token)
    try:
        user_id = int(user_id_str)
    except ValueError:
        logger.error(f"Invalid user ID in token: {user_id_str}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"Fetching favorites for user {user_id}")
    return await bll_get_favorites_by_user(user_id, db)

@router.delete(
    "/{favorite_id}",
    summary="Удалить объявление из избранного",
    response_model=dict
)
async def remove_favorite(
    favorite_id: int,
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_db)
):
    user_id_str = await validate_access_token(access_token)
    try:
        user_id = int(user_id_str)
    except ValueError:
        logger.error(f"Invalid user ID in token: {user_id_str}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"User {user_id} removing favorite {favorite_id}")
    return await bll_delete_favorite(favorite_id, user_id, db)