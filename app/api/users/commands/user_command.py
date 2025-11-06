from fastapi import (
    HTTPException, 
    UploadFile,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.users.schemas.update import UserUpdate
from app.api.users.schemas.response import (
    UserBase, 
    LogoResponse,
)
from app.api.users.crud.user_crud import (
    dal_get_user_by_id, 
    dal_create_logo, 
    dal_update_user,
    dal_delete_logo, 
    dal_get_user_logo, 
)
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
    logo_link = user.user_logos[0].logo.logo_link if user.user_logos else None
    logger.info(f"Returning data for user_id: {user_id}, role: {role_name}")

    return UserBase(
        first_name=user.first_name or "",
        last_name=user.last_name or "",
        surname=user.surname or "",
        email=user.email or "",
        phone_number=user.phone_number or "",
        role=role_name,
        logo_link=logo_link
    )


async def bll_create_logo(user_id: int, logo: UploadFile, db: AsyncSession) -> LogoResponse:
    if not logo.filename.lower().endswith(('png', 'jpg', 'jpeg')):
        logger.error(f"Invalid file type for logo: {logo.filename}")
        raise HTTPException(status_code=400, detail="Поддерживаются только файлы .png, .jpg, .jpeg")
    
    existing_logo = await dal_get_user_logo(user_id, db)
    if existing_logo:
        logger.warning(f"Logo already exists for user_id: {user_id}, logo_id: {existing_logo.logo_id}")
        raise HTTPException(status_code=400, detail="Логотип уже добавлен")
    
    os.makedirs(UPLOAD_LOGO_FOLDER, exist_ok=True)

    filename = f"{uuid.uuid4()}.{logo.filename.split('.')[-1]}"
    save_path = os.path.join(UPLOAD_LOGO_FOLDER, filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(logo.file, buffer)

    logo_obj = await dal_create_logo(user_id=user_id, logo_link=save_path, db=db)
    
    logger.info(f"Logo created for user_id {user_id}, logo_id {logo_obj.id}")
    return LogoResponse(message="Логотип успешно загружен", logo_id=logo_obj.id)


async def bll_update_user(user_id: int, data: UserUpdate, db: AsyncSession) -> UserBase:
    user = await dal_update_user(
        user_id=user_id,
        first_name=data.first_name,
        last_name=data.last_name,
        surname=data.surname,
        phone_number=data.phone_number,
        db=db
    )
    if not user:
        logger.error(F"User with ID {user_id} not found for update")
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if not user.is_active:
        logger.error("User with ID {user_id} is not active")
        raise HTTPException(status_code=400, detail="Пожалуйста, подтвердите email")
    
    role_name = user.user_roles[0].role.role_name if user.user_roles else None
    logo_link = user.user_logos[0].logo.logo_link if user.user_logos else None
    logger.info(f"User data updated for user_id: {user_id}")

    return UserBase(
        first_name=user.first_name or "",
        last_name=user.last_name or "",
        surname=user.surname or "",
        email=user.email or "",
        phone_number=user.phone_number or "",
        role=role_name,
        logo_link=logo_link
    )


async def bll_delete_logo(user_id: int, db: AsyncSession) -> LogoResponse:
    success = await dal_delete_logo(user_id, db)
    if not success:
        logger.error(f"No logo found to delete for user_id: {user_id}")
        raise HTTPException(status_code=404, detail="Логотип не найден")
    
    logger.info(f"Logo deleted for user_id: {user_id}")
    return LogoResponse(message="Логотип успешно удален!")