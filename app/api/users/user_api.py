from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.users.schemas.response import UserBase, LogoResponse
from app.api.users.schemas.update import UserUpdate
from app.api.users.commands.user_command import (bll_get_user_data, bll_create_logo, bll_update_user,
                                                 bll_delete_logo, )
from database.db import get_db
from util.context_utils import get_access_token, validate_access_token
import logging


logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "",
    summary="Данные Пользователя",
    response_model=UserBase
)
async def user_data(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    try:
        user_id = int(await validate_access_token(access_token))
    except ValueError:
        logger.error(f"Invalid user ID in token: {access_token}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"Fetching data for user_id: {user_id}")
    return await bll_get_user_data(user_id, db)


@router.post(
    "/logo",
    summary="Загрузить логотип пользователя",
    response_model=LogoResponse
)
async def create_logo(access_token: str = Depends(get_access_token), logo: UploadFile = File(...),db: AsyncSession = Depends(get_db)):
    try:
        user_id = int(await validate_access_token(access_token))
    except ValueError:
        logger.error(f"Invalid user ID in token: {access_token}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    logger.info(f"User {user_id} uploading logo")
    return await bll_create_logo(user_id, logo, db)


@router.put(
    "",
    summary="Редактировать профиль пользователя",
    response_model=UserBase
)
async def update_user(data: UserUpdate, access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    try:
        user_id = int(await validate_access_token(access_token))
    except ValueError:
        logger.info(f"Invalid user ID in token {access_token}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"User {user_id} updating profile")
    return await bll_update_user(user_id, data, db)


@router.delete(
    "/logo",
    summary="Удалить логотип пользователя",
    response_model=LogoResponse
)
async def delete_logo(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    try:
        user_id = int(await validate_access_token(access_token))
    except ValueError:
        logger.info(f"Invalid user ID in token {access_token}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"User {user_id} deleting logo")
    return await bll_delete_logo(user_id, db)