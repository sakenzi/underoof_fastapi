from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query
from app.api.nearest_geolocations.commands.nearest_geo_crud import get_nearest_geolocations
from typing import List
from database.db import get_db
from app.api.advertisements.schemas.response import AdvertisementsResponse


router = APIRouter()

@router.get(
    "",
    summary="Получить ближайшие объявления",
    response_model=List[AdvertisementsResponse]
)
async def get_nearby_ads(
    latitude: float = Query(..., description="Широта"),
    longitude: float = Query(..., description="Долгота"),
    radius: float = Query(0.005, description="Радиус в градусах (~500 м)"),
    db: AsyncSession = Depends(get_db)
):
    return await get_nearest_geolocations(latitude=latitude, longitude=longitude, radius=radius, db=db)