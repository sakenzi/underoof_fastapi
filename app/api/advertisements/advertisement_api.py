from fastapi import APIRouter, Depends, Request, HTTPException, Form, UploadFile, File, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.advertisements.schemas.create import CreateAdvertisementByTenant, CreateAdvertisementByLandlord
from app.api.advertisements.schemas.response import AdvertisementResponse, AdvertisementListResponse
from app.api.advertisements.commands.adv_command import (
    bll_create_advertisement_by_tenant, bll_create_advertisement_by_landlord,
    bll_get_advertisements_by_user, bll_get_landlord_advertisements_for_tenant,
    bll_get_tenant_advertisements_for_landlord, bll_get_advertisement_by_id,
    bll_get_advertisements_by_filter
)
from database.db import get_db
from util.context_utils import get_access_token, validate_access_token
from datetime import date
from typing import List, Optional
import logging


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/advertisements")

@router.post(
    "/tenant/create",
    summary="Создать объявление от арендатора",
    response_model=AdvertisementResponse
)
async def add_advertisement_by_tenant(
    request: Request,
    data: CreateAdvertisementByTenant,
    db: AsyncSession = Depends(get_db)
):
    access_token = await get_access_token(request)
    user_id_str = await validate_access_token(access_token)
    try:
        user_id = int(user_id_str)
    except ValueError:
        logger.error(f"Invalid user ID in token: {user_id_str}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"User {user_id} creating tenant advertisement")
    return await bll_create_advertisement_by_tenant(user_id, data, db)

@router.post(
    "/landlord/create",
    summary="Создать объявление от арендодателя с фото",
    response_model=AdvertisementResponse
)
async def add_advertisement_by_landlord(
    request: Request,
    description: str = Form(...),
    number_of_room: int = Form(...),
    quadrature: float = Form(...),
    floor: int = Form(...),
    price: int = Form(...),
    from_the_date: date = Form(...),
    before_the_date: date = Form(...),
    location_id: int = Form(...),
    type_advertisement_id: int = Form(...),
    photos: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    access_token = await get_access_token(request)
    user_id_str = await validate_access_token(access_token)
    try:
        user_id = int(user_id_str)
    except ValueError:
        logger.error(f"Invalid user ID in token: {user_id_str}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")

    data = CreateAdvertisementByLandlord(
        description=description,
        number_of_room=number_of_room,
        quadrature=quadrature,
        floor=floor,
        price=price,
        from_the_date=from_the_date,
        before_the_date=before_the_date,
        location_id=location_id,
        type_advertisement_id=type_advertisement_id,
        photos=photos
    )
    logger.info(f"User {user_id} creating landlord advertisement with {len(photos)} photos")
    return await bll_create_advertisement_by_landlord(user_id, data, db)

@router.get(
    "/all/user",
    response_model=List[AdvertisementListResponse],
    summary="Получить все объявления пользователя"
)
async def get_my_advertisements(
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_db)
):
    user_id_str = await validate_access_token(access_token)
    try:
        user_id = int(user_id_str)
    except ValueError:
        logger.error(f"Invalid user ID in token: {user_id_str}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"Fetching advertisements for user {user_id}")
    return await bll_get_advertisements_by_user(user_id, db)

@router.get(
    "/all/tenants",
    response_model=List[AdvertisementListResponse],
    summary="Арендатор получает объявления от арендодателей"
)
async def get_ads_from_landlords_for_tenant(
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_db)
):
    user_id_str = await validate_access_token(access_token)
    try:
        user_id = int(user_id_str)
    except ValueError:
        logger.error(f"Invalid user ID in token: {user_id_str}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"Tenant user {user_id} fetching landlord advertisements")
    return await bll_get_landlord_advertisements_for_tenant(user_id, db)

@router.get(
    "/all/landlords",
    response_model=List[AdvertisementListResponse],
    summary="Арендодатель получает объявления от арендаторов"
)
async def get_ads_from_tenants_for_landlord(
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_db)
):
    user_id_str = await validate_access_token(access_token)
    try:
        user_id = int(user_id_str)
    except ValueError:
        logger.error(f"Invalid user ID in token: {user_id_str}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"Landlord user {user_id} fetching tenant advertisements")
    return await bll_get_tenant_advertisements_for_landlord(user_id, db)

@router.get(
    "/filter",
    response_model=List[AdvertisementListResponse],
    summary="Список объявлений с фильтрами"
)
async def get_ads_by_filter(
    type_advertisement_id: Optional[int] = Query(None),
    location_id: Optional[int] = Query(None),
    min_price: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    city_id: Optional[int] = Query(None),
    street_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    response: Response = None,
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Fetching advertisements with filters: type={type_advertisement_id}, location={location_id}, price=[{min_price}, {max_price}], dates=[{from_date}, {to_date}], city={city_id}, street={street_id}")
    items, total = await bll_get_advertisements_by_filter(
        db, type_advertisement_id, location_id, min_price, max_price,
        from_date, to_date, city_id, street_id, limit, offset
    )
    if response is not None:
        response.headers["X-Total-Count"] = str(total)
    return items

@router.get(
    "/advertisement/{ad_id}",
    response_model=AdvertisementListResponse,
    summary="Получить объявление по ID"
)
async def get_ad_by_id(ad_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Fetching advertisement ID {ad_id}")
    return await bll_get_advertisement_by_id(ad_id, db)