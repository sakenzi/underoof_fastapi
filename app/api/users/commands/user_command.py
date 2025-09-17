from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.users.schemas.create import UserBase, LogoResponse
from app.api.users.crud.user_crud import dal_get_user_by_id, dal_create_logo
import logging
import shutil
import uuid
import os


logger = logging.getLogger(__name__)
UPLOAD_LOGO_FOLDER = "uploads/user_logos"

async def bll_get_user_data(user_id: int, db: AsyncSession) -> UserBase:
    user = await dal_get_user_by_id(user_id, db)
    if not user:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if not user.is_active:
        logger.error(f"User with ID {user_id} is not active")
        raise HTTPException(status_code=400, detail="Please verify your email first")

    role_name = user.user_roles[0].role.role_name if user.user_roles else None
    logger.info(f"Returning data for user_id: {user_id}, role: {role_name}")

    return UserBase(
        first_name=user.first_name or "",
        last_name=user.last_name or "",
        surname=user.surname or "",
        email=user.email or "",
        phone_number=user.phone_number or "",
        role=role_name
    )


async def bll_create_logo(user_id: int, logo: UploadFile, db: AsyncSession) -> LogoResponse:
    if not logo.filename.lower().endswith(('png', 'jpg', 'jpeg')):
        logger.error(f"Invalid file type for logo: {logo.filename}")
        raise HTTPException(status_code=400, detail="Поддерживаются только файлы .png, .jpg, .jpeg")
    
    os.makedirs(UPLOAD_LOGO_FOLDER, exist_ok=True)

    filename = f"{uuid.uuid4()}.{logo.filename.split('.')[-1]}"
    save_path = os.path.join(UPLOAD_LOGO_FOLDER, filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(logo.file, buffer)

    logo_obj = await dal_create_logo(user_id=user_id, logo_link=save_path, db=db)
    
    logger.info(f"Logo created for user_id {user_id}, logo_id {logo_obj.id}")
    return LogoResponse(message="Логотип успешно загружен", logo_id=logo_obj.id)