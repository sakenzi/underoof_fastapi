from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.api.user.schemas.create import UserBase

from model.models import User, UserRole

async def dal_user_data(user_id: int, db: AsyncSession) -> UserBase:
    result = await db.execute(
        select(User)
        .options(
            joinedload(User.user_roles).joinedload(UserRole.role)
        )
        .filter(User.id == user_id)
    )

    user = result.unique().scalar_one_or_none()

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Please verify your email first")

    role_name = None
    if user.user_roles:
        role_name = user.user_roles[0].role.role_name 

    return UserBase(
        first_name=user.first_name,
        last_name=user.last_name,
        surname=user.surname,
        email=user.email,
        phone_number=user.phone_number,
        role=role_name
    )