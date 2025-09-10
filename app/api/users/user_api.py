from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.users.schemas.create import UserBase
from app.api.users.commands.user_command import bll_get_user_data
from database.db import get_db
from util.context_utils import get_access_token, validate_access_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/",
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