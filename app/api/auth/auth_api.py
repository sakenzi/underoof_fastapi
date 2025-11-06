from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.schemas.create import (
    EmailRequest, 
    VerifyEmail, 
    UserCreate, 
    UserLogin, 
    UserLoginBase
)
from app.api.auth.schemas.response import (
    TokenResponse, 
    MessageResponse,
)
from app.api.auth.schemas.sms_create import (
    PhoneVerifyCode, 
    PhoneVerifyRequest,
)
from app.api.auth.commands.auth_command import (
    bll_send_verification_code,
    bll_verify_email,
    bll_user_register,
    bll_user_login,
)
from app.api.auth.commands.auth_sms_command import (
    bll_user_login_base,
    bll_send_phone_code,
    bll_verify_phone_code,
)
from database.db import get_db


router = APIRouter()

@router.post("/email/send", response_model=TokenResponse, summary="Отправить код подтверждения на email")
async def send_code(req: EmailRequest, db: AsyncSession = Depends(get_db)):
    return await bll_send_verification_code(req, db)


@router.post("/email/verify/{token}", response_model=TokenResponse, summary="Подтвердить код из письма")
async def verify_email(token: str, req: VerifyEmail, db: AsyncSession = Depends(get_db)):
    return await bll_verify_email(token, req, db)


@router.post("/phone/send", response_model=MessageResponse, summary="Отправить код на номер телефона")
async def send_phone_code(req: PhoneVerifyRequest, db: AsyncSession = Depends(get_db)):
    return await bll_send_phone_code(req, db)


@router.post("/phone/verify", response_model=MessageResponse, summary="Подтвердить номер телефона")
async def verify_phone_code(req: PhoneVerifyCode, db: AsyncSession = Depends(get_db)):
    return await bll_verify_phone_code(req, db)


@router.post("/register", response_model=TokenResponse, summary="Регистрация нового пользователя")
async def register_user(req: UserCreate, db: AsyncSession = Depends(get_db)):
    return await bll_user_register(req, db)


@router.post("/login", response_model=TokenResponse, summary="Логин по email и паролю")
async def login_user(req: UserLogin, db: AsyncSession = Depends(get_db)):
    return await bll_user_login(req, db)


@router.post("/login/base", response_model=TokenResponse, summary="Логин по email или по телефону и паролю")
async def login_base_user(req: UserLoginBase, db: AsyncSession = Depends(get_db)):
    return await bll_user_login_base(req, db)