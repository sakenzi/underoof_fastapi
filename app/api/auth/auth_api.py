# from app.api.auth.schemas.create import PhoneNumberInput, VerifyPhoneInput, UserLogin, UserRegister
# from app.api.auth.commands.auth_crud import (send_verification_code, verify_phone_and_register,
#                                              user_login, user_register, )
from app.api.auth.schemas.create import EmailRequest, UserCreate, UserLogin, VerifyEmail
from app.api.auth.commands.auth_crud import send_verification_code_request, user_register, user_login, verify_user_email
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from app.api.auth.schemas.response import TokenResponse


router = APIRouter()


# @router.post(
#     '/send-code',
#     summary="Отправить код подтверждения по номеру",
# )
# async def send_code(phone: PhoneNumberInput, db: AsyncSession = Depends(get_db)):
#     return await send_verification_code(phone, db)


# @router.post(
#     '/verify-phone',
#     summary="Проверка кода и регистрация",
#     response_model=TokenResponse
# )
# async def verify_phone(data: VerifyPhoneInput, db: AsyncSession = Depends(get_db)):
#     return await verify_phone_and_register(data, db)


# @router.post(
#     '/register',
#     summary="Регистрация без подтверждение номера",
#     response_model=TokenResponse
# )
# async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
#     return await user_register(user=user, db=db)


# @router.post(
#     '/login',
#     summary="Login пользователя",
#     response_model=TokenResponse
# )
# async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
#     return await user_login(phone_number=login_data.phone_number, password=login_data.password, db=db)

@router.post(
    '/user/send_email',
    summary='Отправить код подтверждения на электронную почту'
)
async def send_verification(email_request: EmailRequest, db: AsyncSession = Depends(get_db)):
    return await send_verification_code_request(email_request=email_request, db=db)


@router.post(
    '/user/register',
    summary="Регистрация пользователя"
)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_register(user=user, db=db)


@router.post(
    '/user/login',
    summary='Логин пользователя',
    # response_model=TokenResponse
)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await user_login(email=login_data.email, password=login_data.password, db=db)


@router.post(
    '/user/verify/{token}',
    summary="Подтвердите адрес электронной почты пользователя с помощью токена и кода"
)
async def verify_email(token: str, verify_data: VerifyEmail, db: AsyncSession = Depends(get_db)):
    return await verify_user_email(token=token, code=verify_data.code, db=db)