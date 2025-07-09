from model.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException
from app.api.auth.schemas.create import PhoneNumberInput, VerifyPhoneInput
from util.context_utils import hash_password, create_access_token
from app.api.auth.schemas.response import TokenResponse
import random
from app.api.auth.commands.sms_service import send_sms  
from datetime import datetime, timedelta, timezone


CODE_EXPIRATION_MINUTES = 5

async def send_verification_code(data: PhoneNumberInput, db: AsyncSession):
    stmt = await db.execute(select(User).filter_by(phone_number=data.phone_number))
    record = stmt.scalar_one_or_none()

    code = str(random.randint(1000, 9999))
    
    if record:
        record.code = code
        record.created_at = datetime.utcnow()
    else:
        record = User(phone_number=data.phone_number, code=code)
        db.add(record)

    await db.commit()

    sent = send_sms(data.phone_number, f"Ваш код подтверждения: {code}")
    if not sent:
        raise HTTPException(status_code=500, detail="Ошибка отправки СМС")
    
    return {"message": "Код отправлен"}

async def verify_phone_and_register(data: VerifyPhoneInput, db: AsyncSession):
    stmt = await db.execute(select(User).filter_by(phone_number=data.phone_number))
    record = stmt.scalar_one_or_none()

    if not record or record.code != data.code:
        raise HTTPException(status_code=400, detail="Неверный код")

    now = datetime.now(timezone.utc)
    if now - record.created_at > timedelta(minutes=CODE_EXPIRATION_MINUTES):
        raise HTTPException(status_code=400, detail="Код истёк")

    record.is_verified = True
    
    stmt_user = await db.execute(select(User).filter(User.username == data.username))
    if stmt_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = hash_password(data.password)
    user = User(
        username=data.username,
        password=hashed_password,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    access_token, expire_time = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time
    )