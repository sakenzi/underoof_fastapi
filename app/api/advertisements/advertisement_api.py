from fastapi import APIRouter, Depends, Request, HTTPException, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import List
from database.db import get_db
from app.api.advertisements.commands.advertisement_crud import create_advertisement_by_lessee, create_advertisement_by_seller
from app.api.advertisements.schemas.create import CreateAdvertisementByLessee, CreateAdvertisementBySeller
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