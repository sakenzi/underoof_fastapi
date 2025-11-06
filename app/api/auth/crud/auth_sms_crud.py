from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from model.models import (
    User, 
    UserRole, 
    PhoneCode,
)
from fastapi import HTTPException   
from sqlalchemy.orm import joinedload
from app.api.auth.commands.phone import normalize_phone
import re


async def dal_get_user_by_login(login: str, db: AsyncSession) -> User | None:
    if re.match(r"^\+?\d+$", login):
        login = normalize_phone(login)
    result = await db.execute(
        select(User)
        .options(joinedload(User.user_roles).joinedload(UserRole.role))
        .where(
            (User.email == login) | (User.phone_number == login)
        )
    )
    return result.unique().scalar_one_or_none()


async def dal_save_phone_code(phone: str, code: str, db: AsyncSession) -> PhoneCode:
    result = await db.execute(select(PhoneCode).where(PhoneCode.phone_number == phone))
    phone_code = result.scalar_one_or_none()
    if not phone_code:
        phone_code = PhoneCode(phone_number=phone, code=code, is_verified=False)
        db.add(phone_code)
    else:
        phone_code.code = code
        phone_code.is_verified = False
    await db.commit()
    await db.refresh(phone_code)
    return phone_code


async def dal_verify_phone_code(phone: str, code: str, db: AsyncSession) -> PhoneCode | None:
    try:
        normalized_phone = normalize_phone(phone)
    except ValueError:
        return None
    query = select(PhoneCode).where(PhoneCode.phone_number == normalized_phone)
    if code:
        query = query.where(PhoneCode.code == code)
    res = await db.execute(query)
    phone_code = res.scalar_one_or_none()
    
    if phone_code and code and phone_code.code == code:
        await db.execute(
            update(PhoneCode)
            .where(PhoneCode.phone_number == normalized_phone)
            .values(is_verified=True)
        )
        await db.commit()
        await db.refresh(phone_code)
    
    return phone_code


async def dal_bind_verified_phone_to_user(user_id: int, phone: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one()
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    user.phone_number = phone
    await db.commit()
    await db.refresh(user)
    return user


async def dal_get_user_by_phone(phone: str, db: AsyncSession) -> User | None:
    try:
        normalized_phone = normalize_phone(phone)
    except ValueError:
        return None
    res = await db.execute(
        select(User)
        .options(joinedload(User.user_roles).joinedload(UserRole.role))
        .where(User.phone_number == normalized_phone)
    )
    return res.unique().scalar_one_or_none()