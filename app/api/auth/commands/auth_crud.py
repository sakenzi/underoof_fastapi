from model.models import User, PhoneCode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException
from app.api.auth.schemas.create import EmailRequest, UserCreate
from util.context_utils import hash_password, create_access_token, verify_password
from app.api.auth.schemas.response import TokenResponse
import random
# from app.api.auth.commands.sms_service import send_sms  
from app.api.auth.commands.sms_service_p1 import send_sms
from datetime import datetime, timezone
from app.api.auth.commands.send_email import generate_verification_code, send_verification_email
from jose import JWTError, jwt
from core.config import settings


# CODE_EXPIRATION_MINUTES = 5

# async def send_verification_code(data: PhoneNumberInput, db: AsyncSession):
#     stmt = await db.execute(select(PhoneCode).filter_by(phone_number=data.phone_number))
#     record = stmt.scalar_one_or_none()

#     code = str(random.randint(1000, 9999))

#     if record:
#         record.code = code
#         record.created_at = datetime.now(timezone.utc)
#     else:
#         record = PhoneCode(phone_number=data.phone_number, code=code)
#         db.add(record)

#     await db.commit()

#     sent = send_sms(data.phone_number, f"Ваш код подтверждения: {code}")
#     if not sent:
#         raise HTTPException(status_code=500, detail="Ошибка отправки СМС")

#     return {"message": "Код отправлен"}


# async def verify_phone_and_register(data: VerifyPhoneInput, db: AsyncSession):
#     stmt = await db.execute(select(PhoneCode).filter_by(phone_number=data.phone_number))
#     record = stmt.scalar_one_or_none()

#     if not record or record.code != data.code:
#         raise HTTPException(status_code=400, detail="Неверный код")

#     # now = datetime.now(timezone.utc)
#     # if now - record.created_at.replace(tzinfo=None) > timedelta(minutes=CODE_EXPIRATION_MINUTES):
#     #     raise HTTPException(status_code=400, detail="Код истёк")

#     record.is_verified = True

#     stmt_user = await db.execute(select(User).filter(User.username == data.username))
#     if stmt_user.scalar_one_or_none():
#         raise HTTPException(status_code=400, detail="Пользователь уже существует")

#     hashed_password = hash_password(data.password)
#     user = User(
#         username=data.username,
#         phone_number=data.phone_number,
#         password=hashed_password,
#     )
#     db.add(user)
#     await db.commit()
#     await db.refresh(user)

#     access_token, expire_time = create_access_token(data={"sub": str(user.id)})

#     return TokenResponse(
#         access_token=access_token,
#         access_token_expire_time=expire_time
#     )


# async def user_login(phone_number: str, password: str, db: AsyncSession):
#     stmt = await db.execute(select(User).filter(User.phone_number == phone_number))
#     user = stmt.scalar_one_or_none()

#     if not user or not verify_password(password, user.password):
#         raise HTTPException(
#             status_code=401,
#             detail="Неправильный номер или пароль"
#         )
    
#     access_token, expire_time = create_access_token(data={"sub": str(user.id)})

#     return TokenResponse(
#         access_token=access_token,
#         access_token_expire_time=expire_time
#     )


# async def user_register(user: UserRegister, db: AsyncSession):
#     stmt = await db.execute(select(User).filter(User.phone_number==user.phone_number))
#     existing_user = stmt.scalar_one_or_none()
#     if existing_user:
#         raise HTTPException(
#             status_code=400, 
#             detail="User already exists"
#         )
    
#     hashed_password = hash_password(user.password)

#     new_user = User(
#         phone_number=user.phone_number,
#         username=user.username,
#         password=hashed_password,
#     )
#     db.add(new_user)
#     await db.commit()
#     await db.refresh(new_user)  

#     access_token, expire_time = create_access_token(data={"sub": str(new_user.id)})

#     return TokenResponse(
#         access_token=access_token,
#         access_token_expire_time=expire_time,
#     )


async def send_verification_code_request(email_request: EmailRequest, db: AsyncSession) -> TokenResponse:
    stmt = await db.execute(select(User).filter(User.email == email_request.email))
    user = stmt.scalar_one_or_none()
    verification_code = await generate_verification_code()

    if user:
        await db.execute(update(User).where(User.email == email_request.email).values(verification_code=verification_code))
    else:
        new_user = User(
            email=email_request.email,
            verification_code=verification_code,
            is_active=False
        )
        db.add(new_user)

    await db.commit()

    access_token, expire_time = create_access_token(data={"sub": email_request.email})
    await send_verification_email(email_request.email, verification_code)

    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time,
        message="Verification code sent to your email"
    )


async def user_register(user: UserCreate, db: AsyncSession) -> dict:
    stmt = await db.execute(select(User).filter(User.email == user.email))
    existing_user = stmt.scalar_one_or_none()

    hashed_password = hash_password(user.password)

    if existing_user:
        is_active = existing_user.is_active
        verification_code = None if is_active else await generate_verification_code()

        await db.execute(
            update(User)
            .where(User.email == user.email)
            .values(
                username=user.username,
                phone_number=user.phone_number,
                password=hashed_password,
                is_active=is_active,
                verification_code=verification_code
            )
        )
    else:
        verification_code = await generate_verification_code()
        new_user = User(
            username=user.username,
            email=user.email,
            phone_number=user.phone_number,
            password=hashed_password,
            is_active=False,
            verification_code=verification_code
        )
        db.add(new_user)

    await db.commit()


    if existing_user and is_active:
        access_token, expire_time = create_access_token(data={"sub": str(existing_user.id)})
        return TokenResponse(
            access_token=access_token,
            access_token_expire_time=expire_time,
            message="User registered successfully"
        )
    else:
        await send_verification_email(user.email, verification_code)
        return {"message": "User registered successfully, please verify your email"}
    

async def user_login(email: str, password: str, db: AsyncSession) -> TokenResponse:
    stmt = await db.execute(select(User).filter(User.email == email))
    user = stmt.scalar_one_or_none()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Please verify your email first")
    
    access_token, expire_time = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time,
        message="Login successful"
    )


async def verify_user_email(token: str, code: str, db: AsyncSession) -> TokenResponse:
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        email: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    stmt = await db.execute(select(User).filter(User.email == email))
    user = stmt.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.verification_code != code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    await db.execute(
        update(User)
        .where(User.email == email)
        .values(
            is_active=True,
            verification_code=None
        )
    )
    await db.commit()

    access_token, expire_time = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time,
        message="Email verified successfully"
    )