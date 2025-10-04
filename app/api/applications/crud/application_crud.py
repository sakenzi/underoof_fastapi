from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from model.models import (Application, User, Advertisement, 
                          UserRole, UserLogo, Location, Street,
                          AdvertisementPhoto)
import logging
from typing import List


logger = logging.getLogger(__name__)

async def dal_create_application(user_id: int, advertisement_id: int, db: AsyncSession) -> Application:
    application = Application(user_id=user_id, advertisement_id=advertisement_id)
    db.add(application)
    await db.commit()
    await db.refresh(application)
    logger.info(f"Created application ID {application.id} for user_id {user_id} on advertisement_id {advertisement_id}")
    return application


async def dal_get_application_by_user_and_ad(user_id: int, advertisement_id: int, db: AsyncSession) -> Application | None:
    stmt = select(Application).where(Application.user_id == user_id, Application.advertisement_id == advertisement_id)
    result = await db.execute(stmt)
    application = result.scalar_one_or_none()
    logger.info(f"Checked application for user_id {user_id}, advertisement_id {advertisement_id}: {'Found' if application else 'Not found'}")
    return application


async def dal_get_applications_by_user_ads(user_id: int, db: AsyncSession) -> List[Application]:
    stmt = select(Application).join(Advertisement).join(UserRole).where(
        UserRole.user_id == user_id,
        Advertisement.user_role_id == UserRole.id
    ).options(
        selectinload(Application.user)
            .selectinload(User.user_logos)
            .selectinload(UserLogo.logo),
        selectinload(Application.advertisement)
            .selectinload(Advertisement.location)
            .selectinload(Location.street)
            .selectinload(Street.city),
        selectinload(Application.advertisement)
            .selectinload(Advertisement.type_advertisement),
        selectinload(Application.advertisement)
            .selectinload(Advertisement.advertisement_photos)
            .selectinload(AdvertisementPhoto.photo)
    )
    result = await db.execute(stmt)
    applications = result.scalars().all()
    logger.info(f"Retrieved {len(applications)} applications for user_id {user_id}'s advertisements")
    return applications


async def dal_get_application_by_id(application_id: int, db: AsyncSession) -> Application | None:
    stmt = select(Application).where(Application.id == application_id)
    result = await db.execute(stmt)
    application = result.scalar_one_or_none()
    logger.info(f"Checked application ID {application_id}: {'Found' if application else 'Not found'}")
    return application


async def dal_delete_application_by_id(application_id: int, db: AsyncSession) -> None:
    stmt = select(Application).where(Application.id == application_id)
    result = await db.execute(stmt)
    application = result.scalar_one_or_none()
    await db.delete(application)
    await db.commit()
    logger.info(f"Application ID {application_id} deleted successfully")