from app.api.auth.schemas.create import UserLoginBase
from app.api.auth.schemas.response import TokenResponse, UserBase, MessageResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.crud.auth_sms_crud import (
    dal_get_user_by_login, 
    dal_save_phone_code, 
    dal_verify_phone_code, 
    dal_get_user_by_phone,
)
from util.context_utils import (
    verify_password, 
    create_access_token,
)
from fastapi import HTTPException
from app.api.auth.crud.auth_crud import dal_get_user_by_email
from app.api.auth.schemas.sms_create import PhoneVerifyCode, PhoneVerifyRequest
from app.api.auth.commands.phone import (
    normalize_phone,
)
import random
import requests
import redis
import logging
from core.config import settings
from os.path import (
    join, 
    dirname,
)
from dotenv import load_dotenv
from urllib.parse import quote


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

logger = logging.getLogger(__name__)

redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
    max_connections=10
)
r = redis.Redis(connection_pool=redis_pool)

MOBIZON_URL = "https://api.mobizon.kz/service/message/sendSmsMessage"

async def bll_user_login_base(req: UserLoginBase, db: AsyncSession) -> TokenResponse:
    user = None
    if "@" in req.login:
        user = await dal_get_user_by_email(req.login, db)
    else:
        try:
            normalized_login = normalize_phone(req.login.strip())
            user = await dal_get_user_by_phone(normalized_login, db)
        except ValueError:
            user = None

    if not user or not verify_password(req.password, user.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Аккаунт не активирован")
    
    access_token, expire_time = create_access_token(data={"sub": str(user.id)})
    role_name = user.user_roles[0].role.role_name if user.user_roles else None

    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time,
        message="Вход успешен",
        user=UserBase(
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            surname=user.surname or "",
            email=user.email or "",
            phone_number=user.phone_number or "",
            role=role_name
        )
    )


async def bll_send_phone_code(req: PhoneVerifyRequest, db: AsyncSession) -> MessageResponse:
    try:
        phone = normalize_phone(req.phone.strip())  
    except ValueError as e:
        logger.error(f"Invalid phone number format: {req.phone}")
        raise HTTPException(400, f"Неверный формат номера телефона: {str(e)}")

    existing_user = await dal_get_user_by_phone(phone, db)
    if existing_user:
        logger.warning(f"Phone {phone} already bound to user {existing_user.id}")
        raise HTTPException(400, "Этот номер уже привязан к другому аккаунту")

    code = f"{random.randint(100000, 999999):06d}"
    logger.info(f"SMS code {code} for {phone}")

    r.setex(f"phone_verify:{phone}", 300, code)
    await dal_save_phone_code(phone, code, db)

    text = quote(f"Код подтверждения номера: {code}")  
    url = (
        f"{MOBIZON_URL}?"
        f"recipient={phone}&"
        f"text={text}&"
        f"apiKey={settings.MOBIZON_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        res = response.json()
        logger.info(f"Mobizon response: {res}")
        if res.get("code") != 0:
            error_msg = res.get("data", {}).get("recipient", res.get("message", "Unknown error"))
            logger.error(f"Mobizon error: {res}")
            raise HTTPException(400, f"Ошибка отправки SMS: {error_msg}")
    except requests.RequestException as e:
        logger.error(f"SMS send failed: {e}")
        raise HTTPException(500, "Не удалось отправить SMS")

    logger.info(f"SMS sent successfully to {phone}")
    return MessageResponse(message="Код отправлен на номер")


async def bll_verify_phone_code(
    req: PhoneVerifyCode,
    db: AsyncSession,
) -> MessageResponse:
    phone = req.phone.strip()
    code = req.code

    redis_code = r.get(f"phone_verify:{phone}")
    if not redis_code or redis_code != code:
        db_code = await dal_verify_phone_code(phone, code, db)
        if not db_code:
            logger.error(f"Invalid or expired code for {phone}")
            raise HTTPException(400, "Неверный или истёкший код")
    else:
        await dal_verify_phone_code(phone, code, db)
        r.delete(f"phone_verify:{phone}")

    logger.info(f"Phone {phone} verified successfully")
    return MessageResponse(message="Номер телефона успешно подтверждён")