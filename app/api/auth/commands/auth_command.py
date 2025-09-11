from fastapi import HTTPException
import re
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.schemas.create import EmailRequest, VerifyEmail, UserCreate, UserLogin
from app.api.auth.schemas.response import MessageResponse, TokenResponse, UserBase, TokenRegisterResponse
from app.api.auth.crud.auth_crud import (
    dal_get_user_by_email,
    dal_upsert_verification_code,
    dal_get_user_by_verification_code,
    dal_clear_verification_code,
    dal_create_user,
    dal_get_user_with_roles_by_email
)
from util.context_utils import hash_password, verify_password, create_access_token
from app.api.auth.commands.send_email import generate_verification_code, send_verification_email
from jose import JWTError, jwt
from core.config import settings


async def _validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(400, "Пароль должен содержать минимум 8 символов.")
    if not re.search(r"[A-Za-z]", password):
        raise HTTPException(400, "Пароль должен содержать хотя бы одну букву.")
    if not re.search(r"\d", password):
        raise HTTPException(400, "Пароль должен содержать хотя бы одну цифру.")


async def bll_send_verification_code(req: EmailRequest, db: AsyncSession) -> TokenResponse:
    user = await dal_get_user_by_email(req.email, db)
    if user and user.is_active:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже зарегистрирован и активен. Пожалуйста, войдите или используйте другой email.")

    code = await generate_verification_code()
    await dal_upsert_verification_code(email=req.email, code=code, db=db)
    access_token, expire_time = create_access_token(data={"sub": req.email})
    await send_verification_email(req.email, code)

    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time,
        message="Verification code sent to your email",
        user=None
    )


async def bll_verify_email(token: str, req: VerifyEmail, db: AsyncSession) -> TokenResponse:
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await dal_get_user_by_verification_code(req.code, db)
    if not user or user.email != email:
        raise HTTPException(400, detail="Неверный код")

    user = await dal_clear_verification_code(email, db)
    access_token, expire_time = create_access_token(data={"sub": str(user.id)})
    role_name = user.user_roles[0].role.role_name if user and user.user_roles else None

    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time,
        message="Email verified successfully",
        user=UserBase(
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            surname=user.surname or "",
            email=user.email or "",
            phone_number=user.phone_number or "",
            role=role_name
        )
    )


async def bll_user_register(req: UserCreate, db: AsyncSession) -> MessageResponse:
    await _validate_password(req.password)

    user = await dal_get_user_by_email(req.email, db)
    if not user:
        raise HTTPException(400, detail="Email не найден. Пожалуйста, запросите код верификации.")

    if user.verification_code is not None:
        raise HTTPException(400, detail="Email не подтверждён. Пожалуйста, подтвердите email с помощью кода.")

    data = req.dict()
    data["password"] = hash_password(req.password)
    await dal_create_user(data=data, db=db)

    access_token, expire_time = create_access_token(data={"sub": str(user.id)})
    
    return TokenRegisterResponse(
        access_token=access_token,
        access_token_expire_time=expire_time,
        message="Login successful",
    )


async def bll_user_login(req: UserLogin, db: AsyncSession) -> TokenResponse:
    user = await dal_get_user_with_roles_by_email(req.email, db)
    if not user or not verify_password(req.password, user.password):
        raise HTTPException(401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(400, detail="Please verify your email first")

    access_token, expire_time = create_access_token(data={"sub": str(user.id)})
    role_name = user.user_roles[0].role.role_name if user.user_roles else None

    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time,
        message="Login successful",
        user=UserBase(
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            surname=user.surname or "",
            email=user.email or "",
            phone_number=user.phone_number or "",
            role=role_name
        )
    )