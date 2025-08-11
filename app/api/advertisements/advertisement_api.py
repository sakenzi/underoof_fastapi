from fastapi import APIRouter, Depends, Request, HTTPException, Form, UploadFile, File, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import List, Optional
from database.db import get_db
from app.api.advertisements.commands.advertisement_crud import (create_advertisement_by_lessee, create_advertisement_by_seller,
                                                                get_advertisements_by_user, get_all_seller_advertisements_for_lessee,
                                                                get_all_lessee_advertisements_for_seller, get_advertisement_by_id,
                                                                get_advertisements_by_filter, )
from app.api.advertisements.schemas.create import CreateAdvertisementByLessee, CreateAdvertisementBySeller
from app.api.advertisements.schemas.response import AdvertisementsResponse, AdvertisementResponse
from util.context_utils import validate_access_token, get_access_token


router = APIRouter()

@router.post(
    '/lessee/create',
    summary="Создать объявление от арендатора"
)
async def add_advertisement_by_lessee(request: Request, data: CreateAdvertisementByLessee, db: AsyncSession = Depends(get_db)):
    access_token = await get_access_token(request)
    user_id_str = await validate_access_token(access_token)

    try: 
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    return await create_advertisement_by_lessee(user_id=user_id, data=data, db=db)


@router.post(
    '/seller/create',
    summary="Создать объявление от продавца с фото"
)
async def add_advertisement_by_seller(
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
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")

    return await create_advertisement_by_seller(
        user_id=user_id,
        data={
            "description": description,
            "number_of_room": number_of_room,
            "quadrature": quadrature,
            "floor": floor,
            "price": price,
            "from_the_date": from_the_date,
            "before_the_date": before_the_date,
            "location_id": location_id,
            "type_advertisement_id": type_advertisement_id,
            "photos": photos
        },
        db=db
    )


@router.get(
    '/all/user',
    response_model=List[AdvertisementsResponse],
    summary="Получить все обьявление пользователя"
)
async def get_my_advertisements(access_token = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    user_id_str = await validate_access_token(access_token)
    user_id = int(user_id_str)
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    return await get_advertisements_by_user(user_id=user_id, db=db)


@router.get(
    '/all/lessee',
    response_model=List[AdvertisementsResponse],
    summary="Арендатор получает объявления от продавцов"
)
async def get_ads_from_sellers_for_lessee(access_token = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    user_id_str = await validate_access_token(access_token)
    user_id = int(user_id_str)
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    return await get_all_seller_advertisements_for_lessee(user_id=user_id, db=db)


@router.get(
    '/all/seller',
    response_model=List[AdvertisementsResponse],
    summary="Продавец получает обьявления от арендатора"
)
async def get_ads_from_lessee_for_seller(access_token = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    user_id_str = await validate_access_token(access_token)
    user_id = int(user_id_str)
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="евалидный ID пользователя в токене")
    return await get_all_lessee_advertisements_for_seller(user_id=user_id, db=db)


@router.get(
    "/filter",
    response_model=List[AdvertisementResponse],
    summary="Список объявлений с фильтрами",
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
    db: AsyncSession = Depends(get_db),
):
    items, total = await get_advertisements_by_filter(
        db=db,
        type_advertisement_id=type_advertisement_id,
        location_id=location_id,
        min_price=min_price,
        max_price=max_price,
        from_date=from_date,
        to_date=to_date,
        city_id=city_id,
        street_id=street_id,
        limit=limit,
        offset=offset,
    )
    if response is not None:
        response.headers["X-Total-Count"] = str(total)
    return items


@router.get(
    '/{ad_id}',
    response_model=AdvertisementResponse,
    summary="Получить объявление по ID"
)
async def get_ad_by_id(ad_id: int, db: AsyncSession = Depends(get_db)):
    return await get_advertisement_by_id(ad_id=ad_id, db=db)