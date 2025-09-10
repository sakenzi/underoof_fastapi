from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from model.models import User, UserRole, Role


async def dal_get_user_by_email(email: str, db: AsyncSession) -> User | None:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()


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
    user = await dal_get_user_by_email(email=data["email"], db=db)
    if user:
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.surname = data.get("surname") or ""
        user.phone_number = data["phone_number"]
        user.password = data["password"]
        user.verification_code = None
        user.is_active = True
        await db.commit()
        await db.refresh(user)
        return user
    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        surname=data.get("surname") or "",
        phone_number=data["phone_number"],
        password=data["password"],
        email=data["email"],
        is_active=False
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