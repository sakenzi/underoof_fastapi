from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.nearest_geolocations.commands.nearest_geo_command import bll_get_nearest_geolocations
from app.api.advertisements.schemas.response import AdvertisementListResponse
from database.db import get_db
from util.context_utils import get_access_token, validate_access_token
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/nearest_geolocations")

@router.get(
    "",
    summary="Получить ближайшие объявления",
    response_model=List[AdvertisementListResponse]
)
async def get_nearby_ads(
    latitude: float = Query(..., description="Широта"),
    longitude: float = Query(..., description="Долгота"),
    radius: float = Query(0.005, description="Радиус в градусах (~500 м)"),
    db: AsyncSession = Depends(get_db),
    access_token: str = Depends(get_access_token)
):
    user_id_str = await validate_access_token(access_token)
    try:
        user_id = int(user_id_str)
    except ValueError:
        logger.error(f"Invalid user ID in token: {user_id_str}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"User {user_id} fetching advertisements near ({latitude}, {longitude}) with radius {radius}")
    return await bll_get_nearest_geolocations(latitude, longitude, radius, db)