from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.api.applications.crud.application_crud import dal_create_application, dal_get_application_by_user_and_ad, dal_get_applications_by_user_ads
from app.api.advertisements.crud.adv_crud import dal_get_user_role, dal_get_advertisement_by_id
from app.api.applications.schemas.response import ApplicationResponse, ApplicationListResponse
from app.api.advertisements.schemas.response import UserResponse, LocationsResponse, StreetsResponse, CitiesResponse, TypeAdvertisementResponse, PhotoResponse
import logging
from typing import List


logger = logging.getLogger(__name__)

async def bll_create_application(user_id: int, advertisement_id: int, db: AsyncSession) -> ApplicationResponse:
    user_role = await dal_get_user_role(user_id, 1, db)
    if not user_role:
        logger.error(f"User {user_id} does not have tenant role (role_id=1)")
        raise HTTPException(status_code=403, detail="Доступ разрешен только арендаторам")
    
    advertisement = await dal_get_advertisement_by_id(advertisement_id, db)
    if not advertisement:
        logger.error(f"Advertisement ID {advertisement_id} not found")
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    if not advertisement.is_active:
        logger.error(f"Advertisement ID {advertisement_id} is not active")
        raise HTTPException(status_code=400, detail="Объявление не активно")
    
    existing_application = await dal_get_application_by_user_and_ad(user_id, advertisement_id, db)
    if existing_application:
        logger.error(f"User {user_id} already applied to advertisement ID {advertisement_id}")
        raise HTTPException(status_code=400, detail="Вы уже оставили отклик на это объявление")
    
    if advertisement.user_role.user_id == user_id:
        logger.error(f"User {user_id} cannot apply to their own advertisement ID {advertisement_id}")
        raise HTTPException(status_code=400, detail="Нельзя оставить отклик на собственное объявление")
    
    application = await dal_create_application(user_id, advertisement_id, db)
    return ApplicationResponse(message="Отклик успешно создан", application_id=application.id)


async def bll_get_applications_by_user_ads(user_id: int, db: AsyncSession) -> List[ApplicationListResponse]:
    user_role = await dal_get_user_role(user_id, 2, db)
    if not user_role:
        logger.error(f"User {user_id} does not have landlord role (role_id=2)")
        raise HTTPException(status_code=403, detail="Доступ разрешен только арендодателям")
    
    applications = await dal_get_applications_by_user_ads(user_id, db)
    results = []
    for app in applications:
        user=app.user
        user_response=UserResponse(
            id=user.id,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            surname=user.surname or "",
            phone_number=user.phone_number or "",
            logo_link=user.user_logos[0].logo.logo_link if user.user_logos else None
        ) if user else None

        advertisement = app.advertisement
        location_response = None
        full_address = None
        if advertisement.location:
            street_response = StreetsResponse(
                id=advertisement.location.street.id,
                street_name=advertisement.location.street.street_name,
                city=CitiesResponse(
                    id=advertisement.location.street.city.id,
                    city_name=advertisement.location.street.city.city_name
                )
            ) if advertisement.location.street else None
            location_response = LocationsResponse(
                id=advertisement.location.id,
                number=advertisement.location.number,
                latitude=advertisement.location.latitude,
                longitude=advertisement.location.longitude,
                street=street_response
            )
            if advertisement.location.street and advertisement.location.street.city:
                full_address = f"г. {advertisement.location.street.city.city_name}, ул. {advertisement.location.street.street_name}, д. {advertisement.location.number}"
            elif advertisement.location.street:
                full_address = f"ул. {advertisement.location.street.street_name}, д. {advertisement.location.number}"
            else:
                full_address = f"д. {advertisement.location.number}"

        type_ad_response = TypeAdvertisementResponse(
            id=advertisement.type_advertisement.id,
            type_name=advertisement.type_advertisement.type_name
        ) if advertisement.type_advertisement else None

        photo_response = [
            PhotoResponse(id=photo.id, photo_link=photo.photo.photo_link)
            for photo in advertisement.advertisement_photos
        ]

        results.append(ApplicationListResponse(
            id=app.id,
            advertisement_id=app.advertisement_id,
            user=user_response,
            created_at=app.created_at
        ))

    logger.info(f"Formatted {len(results)} applications for user_id {user_id}")
    return results