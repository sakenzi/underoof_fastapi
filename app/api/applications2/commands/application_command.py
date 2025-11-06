from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.api.applications2.crud.application_crud import (
    dal_create_application, 
    dal_get_application_by_user_and_ad, 
    dal_get_applications_by_user_ads, 
    dal_delete_application_by_id, 
    dal_get_application_by_id,
    dal_get_applications_by_user,
    dal_get_applications_by_advertisement,
)
from app.api.advertisements.crud.adv_crud import (
    dal_get_user_role, 
    dal_get_advertisement_by_id,
)
from app.api.applications2.schemas.response import (
    ApplicationResponse, 
    ApplicationListResponse, 
    ApplicationTenantListResponse, 
    ApplicationResponseWrapper,
)
from app.api.advertisements.schemas.response import (
    UserResponse, 
    LocationsResponse, 
    StreetsResponse, 
    CitiesResponse, 
    TypeAdvertisementResponse, 
    PhotoResponse, 
    AdvertisementListResponse,
    RoleResponse,
    UserRoleResponse
)
import logging
from typing import List

logger = logging.getLogger(__name__)

def _format_advertisement_response(advertisement, user_id: int) -> AdvertisementListResponse:
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

    user_role_response = None
    if advertisement.user_role:
        user = advertisement.user_role.user
        logo_link = user.user_logos[0].logo.logo_link if user.user_logos else None
        user_response_ad = UserResponse(
            id=user.id,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            surname=user.surname or "",
            phone_number=user.phone_number or "",
            logo_link=logo_link,
        ) if user else None
        role_response = RoleResponse(
            id=advertisement.user_role.role.id,
            role_name=advertisement.user_role.role.role_name
        ) if advertisement.user_role.role else None
        user_role_response = UserRoleResponse(
            id=advertisement.user_role.id,
            user=user_response_ad,
            role=role_response
        )

    is_favourite = any(fav.user_id == user_id for fav in advertisement.favorites)

    return AdvertisementListResponse(
        id=advertisement.id,
        description=advertisement.description,
        number_of_room=advertisement.number_of_room,
        quadrature=advertisement.quadrature,
        floor=advertisement.floor,
        price=advertisement.price,
        number_of_people=advertisement.number_of_people,
        from_the_date=advertisement.from_the_date,
        before_the_date=advertisement.before_the_date,
        location=location_response,
        type_advertisement=type_ad_response,
        photo=photo_response,
        user_role=user_role_response,
        full_address=full_address,
        is_favourite=is_favourite
    )

async def bll_create_application(user_id: int, advertisement_id: int, proposed_advertisement_id: int | None, db: AsyncSession) -> ApplicationResponse:
    advertisement = await dal_get_advertisement_by_id(advertisement_id, user_id, db)
    if not advertisement:
        logger.error(f"Advertisement ID {advertisement_id} not found")
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    if not advertisement.is_active:
        logger.error(f"Advertisement ID {advertisement_id} is not active")
        raise HTTPException(status_code=400, detail="Объявление не активно")
    
    ad_role_id = advertisement.user_role.role.id
    if ad_role_id == 1:
        required_role = 2  # Tenant applies to landlord ad
    elif ad_role_id == 2:
        required_role = 1  # Landlord applies to tenant ad
    else:
        logger.error(f"Invalid role for advertisement ID {advertisement_id}")
        raise HTTPException(status_code=400, detail="Неверный тип объявления")
    
    user_role = await dal_get_user_role(user_id, required_role, db)
    if not user_role:
        logger.error(f"User {user_id} does not have required role {required_role} for advertisement ID {advertisement_id}")
        raise HTTPException(status_code=403, detail="Доступ разрешен только для соответствующей роли")
    
    if proposed_advertisement_id:
        proposed_ad = await dal_get_advertisement_by_id(proposed_advertisement_id, user_id, db)
        if not proposed_ad:
            logger.error(f"Proposed advertisement ID {proposed_advertisement_id} not found")
            raise HTTPException(status_code=404, detail="Предлагаемое объявление не найдено")
        if proposed_ad.user_role.user_id != user_id:
            logger.error(f"User {user_id} does not own proposed advertisement ID {proposed_advertisement_id}")
            raise HTTPException(status_code=403, detail="Вы не являетесь владельцем предлагаемого объявления")
        if proposed_ad.user_role.role.id != required_role:
            logger.error(f"Proposed advertisement ID {proposed_advertisement_id} does not match user role {required_role}")
            raise HTTPException(status_code=400, detail="Предлагаемое объявление должно соответствовать вашей роли")
    
    existing_application = await dal_get_application_by_user_and_ad(user_id, advertisement_id, db)
    if existing_application:
        logger.error(f"User {user_id} already applied to advertisement ID {advertisement_id}")
        raise HTTPException(status_code=400, detail="Вы уже оставили отклик на это объявление")
    
    if advertisement.user_role.user_id == user_id:
        logger.error(f"User {user_id} cannot apply to their own advertisement ID {advertisement_id}")
        raise HTTPException(status_code=400, detail="Нельзя оставить отклик на собственное объявление")
    
    application = await dal_create_application(user_id, advertisement_id, proposed_advertisement_id, db)
    return ApplicationResponse(message="Отклик успешно создан", application_id=application.id)


async def bll_get_applications_by_user_ads(user_id: int, db: AsyncSession) -> ApplicationResponseWrapper:
    user_role = await dal_get_user_role(user_id, 1, db)
    if not user_role:
        logger.error(f"User {user_id} does not have landlord role (role_id=1)")
        raise HTTPException(status_code=403, detail="Доступ разрешен только арендодателям")
    
    applications = await dal_get_applications_by_user_ads(user_id, db)
    results = []
    for app in applications:
        user = app.user
        user_response = UserResponse(
            id=user.id,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            surname=user.surname or "",
            phone_number=user.phone_number or "",
            logo_link=user.user_logos[0].logo.logo_link if user.user_logos else None
        ) if user else None

        advertisement_response = _format_advertisement_response(app.advertisement, user_id)
        proposed_ad_response = _format_advertisement_response(app.proposed_advertisement, user_id) if app.proposed_advertisement else None

        results.append(ApplicationListResponse(
            id=app.id,
            advertisement=advertisement_response,
            user=user_response,
            proposed_advertisement=proposed_ad_response,
            created_at=app.created_at
        ))

    logger.info(f"Formatted {len(results)} applications for user_id {user_id}")
    return ApplicationResponseWrapper(applications=results)


async def bll_delete_application_by_id(application_id: int, user_id: int, db: AsyncSession) -> ApplicationResponse:
    application = await dal_get_application_by_id(application_id, db)
    if not application:
        logger.error(f"Application ID {application_id} not found")
        raise HTTPException(status_code=404, detail="Отклик не найден")
    
    if application.user_id != user_id:
        logger.error(f"User {user_id} not authorized to delete application ID {application_id}")
        raise HTTPException(status_code=403, detail="Доступ запрещен, вы не являетесь автором отклика")
    
    await dal_delete_application_by_id(application_id, db)
    logger.info(f"Application ID {application_id} deleted by user {user_id}")
    return ApplicationResponse(message="Отклик успешно удален", application_id=application_id)


async def bll_get_user_applications(user_id: int, db: AsyncSession) -> List[ApplicationTenantListResponse]:
    user_role = await dal_get_user_role(user_id, 2, db)
    if not user_role:
        logger.error(f"User {user_id} does not have tenant role (role_id=2)")
        raise HTTPException(status_code=403, detail="Доступ разрешен только арендаторам")
    
    applications = await dal_get_applications_by_user(user_id, db)
    results = []
    for app in applications:
        advertisement_response = _format_advertisement_response(app.advertisement, user_id)
        proposed_ad_response = _format_advertisement_response(app.proposed_advertisement, user_id) if app.proposed_advertisement else None

        results.append(ApplicationTenantListResponse(
            id=app.id,
            advertisement=advertisement_response,
            proposed_advertisement=proposed_ad_response,
            created_at=app.created_at
        ))

    logger.info(f"Formatted {len(results)} user applications for user_id {user_id}")
    return results


async def bll_get_landlord_applications(user_id: int, db: AsyncSession) -> List[ApplicationTenantListResponse]:
    user_role = await dal_get_user_role(user_id, 1, db)
    if not user_role:
        logger.error(f"User {user_id} does not have landlord role (role_id=1)")
        raise HTTPException(status_code=403, detail="Доступ разрешен только арендодателям")
    
    applications = await dal_get_applications_by_user(user_id, db)
    results = []
    for app in applications:
        advertisement_response = _format_advertisement_response(app.advertisement, user_id)
        proposed_ad_response = _format_advertisement_response(app.proposed_advertisement, user_id) if app.proposed_advertisement else None

        results.append(ApplicationTenantListResponse(
            id=app.id,
            advertisement=advertisement_response,
            proposed_advertisement=proposed_ad_response,
            created_at=app.created_at
        ))

    logger.info(f"Formatted {len(results)} landlord applications for user_id {user_id}")
    return results


async def bll_get_tenant_received_applications(user_id: int, db: AsyncSession) -> ApplicationResponseWrapper:
    user_role = await dal_get_user_role(user_id, 2, db)
    if not user_role:
        logger.error(f"User {user_id} does not have tenant role (role_id=2)")
        raise HTTPException(status_code=403, detail="Доступ разрешен только арендаторам")
    
    applications = await dal_get_applications_by_user_ads(user_id, db)
    results = []
    for app in applications:
        user = app.user
        user_response = UserResponse(
            id=user.id,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            surname=user.surname or "",
            phone_number=user.phone_number or "",
            logo_link=user.user_logos[0].logo.logo_link if user.user_logos else None
        ) if user else None

        advertisement_response = _format_advertisement_response(app.advertisement, user_id)
        proposed_ad_response = _format_advertisement_response(app.proposed_advertisement, user_id) if app.proposed_advertisement else None

        results.append(ApplicationListResponse(
            id=app.id,
            advertisement=advertisement_response,
            user=user_response,
            proposed_advertisement=proposed_ad_response,
            created_at=app.created_at
        ))

    logger.info(f"Formatted {len(results)} tenant received applications for user_id {user_id}")
    return ApplicationResponseWrapper(applications=results)


async def bll_get_applications_by_advertisement(advertisement_id: int, user_id: int, db: AsyncSession) -> ApplicationResponseWrapper:
    advertisement = await dal_get_advertisement_by_id(advertisement_id, user_id, db)
    if not advertisement:
        logger.error(f"Advertisement ID {advertisement_id} not found")
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    if advertisement.user_role.user_id != user_id:
        logger.error(f"User {user_id} not authorized to view applications for advertisement ID {advertisement_id}")
        raise HTTPException(status_code=403, detail="Доступ запрещен, вы не являетесь владельцем объявления")
    
    applications = await dal_get_applications_by_advertisement(advertisement_id, db)
    results = []
    for app in applications:
        user = app.user
        user_response = UserResponse(
            id=user.id,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            surname=user.surname or "",
            phone_number=user.phone_number or "",
            logo_link=user.user_logos[0].logo.logo_link if user.user_logos else None
        ) if user else None

        advertisement_response = _format_advertisement_response(app.advertisement, user_id)
        proposed_ad_response = _format_advertisement_response(app.proposed_advertisement, user_id) if app.proposed_advertisement else None

        results.append(ApplicationListResponse(
            id=app.id,
            advertisement=advertisement_response,
            user=user_response,
            proposed_advertisement=proposed_ad_response,
            created_at=app.created_at
        ))

    logger.info(f"Formatted {len(results)} applications for advertisement_id {advertisement_id}")
    return ApplicationResponseWrapper(applications=results)