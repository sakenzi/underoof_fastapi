from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.applications2.commands.application_command import (
    bll_create_application, 
    bll_get_applications_by_user_ads, 
    bll_delete_application_by_id, 
    bll_get_user_applications,
    bll_get_landlord_applications, 
    bll_get_tenant_received_applications,
    bll_get_applications_by_advertisement,
)
from app.api.applications2.schemas.response import (
    ApplicationResponse, 
    ApplicationTenantListResponse, 
    ApplicationResponseWrapper,
)
from database.db import get_db
from util.context_utils import (
    get_access_token, 
    validate_access_token,
)
import logging
from typing import List
from pydantic import BaseModel


logger = logging.getLogger(__name__)

router = APIRouter()

class ApplicationCreate(BaseModel):
    advertisement_id: int
    proposed_advertisement_id: int | None = None

@router.post(
    "",
    summary="Оставить отклик на объявление",
    response_model=ApplicationResponse
)
async def create_application(data: ApplicationCreate, access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    try:
        user_id = int(await validate_access_token(access_token))
    except ValueError:
        logger.error(f"Invalid user ID in token: {access_token}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"User {user_id} creating application for advertisement_id {data.advertisement_id} with proposed_advertisement_id {data.proposed_advertisement_id}")
    return await bll_create_application(user_id, data.advertisement_id, data.proposed_advertisement_id, db)

@router.get(
    "",
    summary="Получить отклики на мои объявления (арендодатель)",
    response_model=ApplicationResponseWrapper
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
    summary="Получить свои оставленные отклики (арендатор)",
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

@router.get(
    "/my_offers",
    summary="Получить свои оставленные отклики (арендодатель)",
    response_model=List[ApplicationTenantListResponse]
)
async def get_landlord_applications(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    try:
        user_id = int(await validate_access_token(access_token))
    except ValueError:
        logger.error(f"Invalid user ID in token: {access_token}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"Fetching offers submitted by landlord user_id {user_id}")
    return await bll_get_landlord_applications(user_id, db)

@router.get(
    "/received",
    summary="Получить отклики на мои объявления (арендатор)",
    response_model=ApplicationResponseWrapper
)
async def get_tenant_received_applications(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    try:
        user_id = int(await validate_access_token(access_token))
    except ValueError:
        logger.error(f"Invalid user ID in token: {access_token}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"Fetching received applications for tenant user_id {user_id}'s advertisements")
    return await bll_get_tenant_received_applications(user_id, db)

@router.get(
    "/{advertisement_id}",
    summary="Получить отклики на объявление по ID",
    response_model=ApplicationResponseWrapper
)
async def get_applications_by_advertisement(advertisement_id: int, access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    try:
        user_id = int(await validate_access_token(access_token))
    except ValueError:
        logger.error(f"Invalid user ID in token: {access_token}")
        raise HTTPException(status_code=400, detail="Невалидный ID пользователя в токене")
    
    logger.info(f"Fetching applications for advertisement_id {advertisement_id} by user_id {user_id}")
    return await bll_get_applications_by_advertisement(advertisement_id, user_id, db)