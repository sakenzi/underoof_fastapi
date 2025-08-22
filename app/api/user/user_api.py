from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.user.commands.user_crud import dal_user_data
from app.api.user.schemas.create import UserBase
from database.db import get_db
from util.context_utils import get_access_token, validate_access_token


router = APIRouter()

@router.get(
    '/data',
    summary='Данные Пользователя',
    response_model=UserBase
)
async def user_data(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    user_id = await validate_access_token(access_token=access_token)
    return await dal_user_data(user_id=user_id, db=db)