from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.schemas.create import EmailRequest, VerifyEmail, UserCreate, UserLogin
from app.api.auth.schemas.response import TokenRegisterResponse, TokenResponse
from app.api.auth.commands.auth_command import (
    bll_send_verification_code,
    bll_verify_email,
    bll_user_register,
    bll_user_login,
)
from database.db import get_db


router = APIRouter()

@router.post("/email/send", response_model=TokenResponse, summary="Отправить код подтверждения на email")
async def send_code(req: EmailRequest, db: AsyncSession = Depends(get_db)):
    return await bll_send_verification_code(req, db)


@router.post("/email/verify/{token}", response_model=TokenResponse, summary="Подтвердить код из письма")
async def verify_email(token: str, req: VerifyEmail, db: AsyncSession = Depends(get_db)):
    return await bll_verify_email(token, req, db)


@router.post("/register", response_model=TokenRegisterResponse, summary="Регистрация нового пользователя")
async def register_user(req: UserCreate, db: AsyncSession = Depends(get_db)):
    return await bll_user_register(req, db)


@router.post("/login", response_model=TokenResponse, summary="Логин по email и паролю")
async def login_user(req: UserLogin, db: AsyncSession = Depends(get_db)):
    return await bll_user_login(req, db)