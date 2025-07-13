from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from app.api.advertisements.commands.advertisement_crud import create_advertisement_by_lessee
from app.api.advertisements.schemas.create import CreateAdvertisementByLessee
from util.context_utils import validate_access_token, get_access_token


router = APIRouter()

@router.post(
    '/advertisement/lessee/create',
    summary="Создать объявление от арендатора"
)
async def add_advertisement_by_lessee(request: Request, data: CreateAdvertisementByLessee, db: AsyncSession = Depends(get_db)):
    access_token = get_access_token(request)
    user_id_str = validate_access_token(access_token)

    try: 
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    return await create_advertisement_by_lessee(user_id=user_id, data=data, db=db)