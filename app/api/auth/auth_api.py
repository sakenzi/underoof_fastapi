from app.api.auth.schemas.create import PhoneNumberInput, VerifyPhoneInput, UserLogin, UserRegister
from app.api.auth.commands.auth_crud import (send_verification_code, verify_phone_and_register,
                                             user_login, user_register, )
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from app.api.auth.schemas.response import TokenResponse


router = APIRouter()


@router.post(
    '/send-code',
    summary="Отправить код подтверждения по номеру",
)
async def send_code(phone: PhoneNumberInput, db: AsyncSession = Depends(get_db)):
    return await send_verification_code(phone, db)


@router.post(
    '/verify-phone',
    summary="Проверка кода и регистрация",
    response_model=TokenResponse
)
async def verify_phone(data: VerifyPhoneInput, db: AsyncSession = Depends(get_db)):
    return await verify_phone_and_register(data, db)


@router.post(
    '/register',
    summary="Регистрация без подтверждение номера",
    response_model=TokenResponse
)
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    return await user_register(user=user, db=db)


@router.post(
    '/login',
    summary="Login пользователя",
    response_model=TokenResponse
)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await user_login(phone_number=login_data.phone_number, password=login_data.password, db=db)

