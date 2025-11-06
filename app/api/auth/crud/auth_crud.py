from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from model.models import (
    User, 
    UserRole,
)
from app.api.auth.commands.phone import normalize_phone
from app.api.auth.crud.auth_sms_crud import dal_get_user_by_phone


async def dal_get_user_by_email(email: str, db: AsyncSession) -> User | None:
    res = await db.execute(
        select(User)
        .options(joinedload(User.user_roles).joinedload(UserRole.role))
        .where(User.email == email)
    )
    return res.unique().scalar_one_or_none()


async def dal_upsert_verification_code(email: str, code: str, db: AsyncSession) -> User:
    user = await dal_get_user_by_email(email=email, db=db)
    if user:
        user.verification_code = code
        await db.commit()
        await db.refresh(user)
        return user
    user = User(email=email, verification_code=code, is_active=False)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def dal_get_user_by_verification_code(code: str, db: AsyncSession) -> User | None:
    res = await db.execute(
        select(User)
        .options(
            joinedload(User.user_roles).joinedload(UserRole.role)
        )
        .where(User.verification_code == code)
    )
    return res.unique().scalar_one_or_none()


async def dal_clear_verification_code(email: str, db: AsyncSession) -> User:
    user = await dal_get_user_by_email(email=email, db=db)
    if user:
        user.verification_code = None
        user.is_active = True
        await db.commit()
        await db.refresh(user)
    return user


async def dal_create_user(data: dict, db: AsyncSession) -> User:
    user = await dal_get_user_by_email(data["email"], db) if data.get("email") else None
    if not user and data.get("phone_number"):
        try:
            normalized_phone = normalize_phone(data["phone_number"])
            user = await dal_get_user_by_phone(normalized_phone, db)
        except ValueError:
            user = None
    
    if user:
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.surname = data.get("surname") or ""
        user.email = data.get("email") or user.email
        user.phone_number = data.get("phone_number") or user.phone_number
        user.password = data["password"]
        user.verification_code = None
        user.is_active = True
        await db.commit()
        await db.refresh(user)
    else:
        normalized_phone = normalize_phone(data["phone_number"]) if data.get("phone_number") else ""
        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            surname=data.get("surname") or "",
            email=data.get("email") or "",
            phone_number=normalized_phone,
            password=data["password"],
            is_active=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    return user


async def dal_get_user_with_roles_by_email(email: str, db: AsyncSession) -> User | None:
    result = await db.execute(
        select(User)
        .options(
            joinedload(User.user_roles).joinedload(UserRole.role)
        )
        .where(User.email == email)
    )
    return result.unique().scalar_one_or_none()


async def dal_get_user_with_roles_by_id(user_id: int, db: AsyncSession) -> User | None:
    result = await db.execute(
        select(User)
        .options(
            joinedload(User.user_roles).joinedload(UserRole.role)
        )
        .where(User.id == user_id)
    )
    return result.unique().scalar_one_or_none()