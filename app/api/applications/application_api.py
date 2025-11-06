from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.applications.commands.application_command import (
    bll_create_application, 
    bll_get_applications_by_user_ads, 
    bll_delete_application_by_id, 
    bll_get_user_applications,
)
from app.api.applications.schemas.response import (
    ApplicationResponse, 
    ApplicationListResponse, 
    ApplicationTenantListResponse,
)
from database.db import get_db
from util.context_utils import (
    get_access_token, 
    validate_access_token,
)
import logging
from typing import List


logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "",
    summary="Оставить отклик на объявление",
    response_model=ApplicationResponse
)
async def create_application(advertisement_id: int, access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    try:
        user_id = int(await validate_access_token(access_token))
    except ValueError:
        logger.error(f"Invalid user ID in token: {access_token}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"User {user_id} creating application for advertisement_id {advertisement_id}")
    return await bll_create_application(user_id, advertisement_id, db)

@router.get(
    "",
    summary="Получить отклики на мои объявления",
    response_model=List[ApplicationListResponse]
)
async def get_my_applications(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    try:
        user_id = int(await validate_access_token(access_token))
    except ValueError:
        logger.error(f"Invalid user ID in token: {access_token}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"Fetching applications for user_id {user_id}'s advertisements")
    return await bll_get_applications_by_user_ads(user_id, db)


@router.delete(
     "/{application_id}",
    summary="Удалить свой отклик на объявление",
    response_model=ApplicationResponse
)
async def delete_application(
    application_id: int,
    access_token: str = Depends(get_access_token),
    db: AsyncSession = Depends(get_db)
):
    try:
        user_id = int(await validate_access_token(access_token))
    except ValueError:
        logger.error(f"Invalid user ID in token: {access_token}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"User {user_id} attempting to delete application ID {application_id}")
    return await bll_delete_application_by_id(application_id, user_id, db)


@router.get(
    "/my",
    summary="Получить свои оставленные отклики",
    response_model=List[ApplicationTenantListResponse]
)
async def get_user_applications(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    try:
        user_id = int(await validate_access_token(access_token))
    except ValueError:
        logger.error(f"Invalid user ID in token: {access_token}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"Fetching applications submitted by user_id {user_id}")
    return await bll_get_user_applications(user_id, db)