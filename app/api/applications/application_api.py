from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.advertisements.commands.adv_command import (
    bll_create_advertisement_by_tenant, bll_create_advertisement_by_landlord,
    bll_get_advertisements_by_user, bll_get_landlord_advertisements_for_tenant,
    bll_get_tenant_advertisements_for_landlord, bll_get_advertisement_by_id,
    bll_get_advertisements_by_filter
)
from app.api.applications.commands.application_command import bll_create_application, bll_get_applications_by_user_ads
from app.api.advertisements.schemas.create import CreateAdvertisementByTenant, CreateAdvertisementByLandlord
from app.api.applications.schemas.response import ApplicationResponse, ApplicationListResponse
from app.api.advertisements.schemas.response import AdvertisementResponse, AdvertisementListResponse
from database.db import get_db
from util.context_utils import get_access_token, validate_access_token
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