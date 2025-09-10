from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.users.schemas.create import UserBase
from app.api.users.crud.user_crud import dal_get_user_by_id
import logging


logger = logging.getLogger(__name__)

async def bll_get_user_data(user_id: int, db: AsyncSession) -> UserBase:
    user = await dal_get_user_by_id(user_id, db)
    if not user:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if not user.is_active:
        logger.error(f"User with ID {user_id} is not active")
        raise HTTPException(status_code=400, detail="Please verify your email first")

    role_name = user.user_roles[0].role.role_name if user.user_roles else None
    logger.info(f"Returning data for user_id: {user_id}, role: {role_name}")

    return UserBase(
        first_name=user.first_name or "",
        last_name=user.last_name or "",
        surname=user.surname or "",
        email=user.email or "",
        phone_number=user.phone_number or "",
        role=role_name
    )