from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.advertisements.schemas.create import (
    CreateAdvertisementByTenant, 
    CreateAdvertisementByLandlord,
)
from app.api.advertisements.schemas.response import (
    AdvertisementResponse, 
    AdvertisementListResponse, 
    UserResponse, 
    RoleResponse, 
    UserRoleResponse, 
    TypeAdvertisementResponse, 
    PhotoResponse,
)
from app.api.advertisements.schemas.update import UpdateAdvertisement
from app.api.advertisements.crud.adv_crud import (
    dal_create_advertisement, 
    dal_create_photo, 
    dal_get_user_role, 
    dal_get_location_by_id,
    dal_get_type_advertisement_by_id, 
    dal_get_advertisements_by_user, 
    dal_get_advertisements_by_role,
    dal_get_advertisements_by_filter, 
    dal_get_adv_by_id, 
    dal_update_advertisement, 
    dal_update_photos, 
)
from app.api.addresses.schemas.response import (
    LocationsResponse, 
    StreetsResponse, 
    CitiesResponse,
)
from datetime import date
import uuid
import os
import shutil
import logging
from typing import (
    List, 
    Tuple, 
    Optional,
)
from model.models import Advertisement


logger = logging.getLogger(__name__)

UPLOAD_FOLDER = "uploads/photo_advertisements"

async def bll_create_advertisement_by_tenant(user_id: int, data: CreateAdvertisementByTenant, db: AsyncSession) -> AdvertisementResponse:
    user_role = await dal_get_user_role(user_id, 2, db)
    if not user_role:
        logger.error(f"User {user_id} does not have tenant role (role_id=2)")
        raise HTTPException(status_code=403, detail="Доступ запрещен, требуется роль арендатора")

    if data.location_id:
        location = await dal_get_location_by_id(data.location_id, db)
        if not location:
            logger.error(f"Location ID {data.location_id} not found")
            raise HTTPException(status_code=404, detail="Адрес не найден")

    type_ad = await dal_get_type_advertisement_by_id(data.type_advertisement_id, db)
    if not type_ad:
        logger.error(f"Type advertisement ID {data.type_advertisement_id} not found")
        raise HTTPException(status_code=404, detail="Тип объявления не найден")

    if data.from_the_date > data.before_the_date:
        logger.error(f"Invalid date range: from {data.from_the_date} to {data.before_the_date}")
        raise HTTPException(status_code=400, detail="Дата начала должна быть раньше даты окончания")

    advertisement = await dal_create_advertisement(
        description=data.description,
        number_of_room=data.number_of_room,
        quadrature=data.quadrature,
        floor=data.floor,
        price=data.price,
        number_of_people=data.number_of_people,
        from_the_date=data.from_the_date,
        before_the_date=data.before_the_date,
        location_id=data.location_id,
        type_advertisement_id=data.type_advertisement_id,
        user_role_id=user_role.id,
        db=db
    )
    logger.info(f"Advertisement created by tenant user_id {user_id}, ad_id {advertisement.id}")
    return AdvertisementResponse(message="Объявление успешно создано", ad_id=advertisement.id)


async def bll_create_advertisement_by_landlord(user_id: int, data: CreateAdvertisementByLandlord, db: AsyncSession) -> AdvertisementResponse:
    user_role = await dal_get_user_role(user_id, 1, db)
    if not user_role:
        logger.error(f"User {user_id} does not have landlord role (role_id=1)")
        raise HTTPException(status_code=403, detail="Доступ запрещен, требуется роль арендодателя")

    location = await dal_get_location_by_id(data.location_id, db)
    if not location:
        logger.error(f"Location ID {data.location_id} not found")
        raise HTTPException(status_code=404, detail="Адрес не найден")

    type_ad = await dal_get_type_advertisement_by_id(data.type_advertisement_id, db)
    if not type_ad:
        logger.error(f"Type advertisement ID {data.type_advertisement_id} not found")
        raise HTTPException(status_code=404, detail="Тип объявления не найден")

    if data.from_the_date > data.before_the_date:
        logger.error(f"Invalid date range: from {data.from_the_date} to {data.before_the_date}")
        raise HTTPException(status_code=400, detail="Дата начала должна быть раньше даты окончания")

    if not data.photos:
        logger.error("No photos provided for landlord advertisement")
        raise HTTPException(status_code=400, detail="Требуется хотя бы одна фотография")

    for photo in data.photos:
        if not photo.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            logger.error(f"Invalid file type for photo: {photo.filename}")
            raise HTTPException(status_code=400, detail="Поддерживаются только файлы .png, .jpg, .jpeg")

    advertisement = await dal_create_advertisement(
        description=data.description,
        number_of_room=data.number_of_room,
        quadrature=data.quadrature,
        floor=data.floor,
        price=data.price,
        number_of_people=data.number_of_people,
        from_the_date=data.from_the_date,
        before_the_date=data.before_the_date,
        location_id=data.location_id,
        type_advertisement_id=data.type_advertisement_id,
        user_role_id=user_role.id,
        db=db
    )

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    for photo in data.photos:
        filename = f"{uuid.uuid4()}.{photo.filename.split('.')[-1]}"
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        await dal_create_photo(advertisement.id, save_path, db)

    logger.info(f"Advertisement created by landlord user_id {user_id}, ad_id {advertisement.id} with {len(data.photos)} photos")
    return AdvertisementResponse(message="Объявление с фото создано", ad_id=advertisement.id)


async def bll_update_advertisement(user_id: int, ad_id: int, data: UpdateAdvertisement, db: AsyncSession) -> AdvertisementResponse:
    advertisement = await dal_get_adv_by_id(ad_id, db)
    if not advertisement:
        logger.error(f"Advertisement ID {ad_id} not found")
        raise HTTPException(status_code=404, detail="Объявление не найдено")

    if advertisement.user_role.user_id != user_id:
        logger.error(f"User {user_id} not authorized to update advertisement ID {ad_id}")
        raise HTTPException(status_code=403, detail="Доступ запрещен, вы не являетесь владельцем объявления")

    user_role = await dal_get_user_role(user_id, advertisement.user_role.role_id, db)
    if not user_role:
        logger.error(f"User {user_id} does not have required role for advertisement ID {ad_id}")
        raise HTTPException(status_code=403, detail="Доступ запрещен, требуется соответствующая роль")

    from_date = data.from_the_date or advertisement.from_the_date
    before_date = data.before_the_date or advertisement.before_the_date
    if from_date > before_date:
        logger.error(f"Invalid date range: from {from_date} to {before_date}")
        raise HTTPException(status_code=400, detail="Дата начала должна быть раньше даты окончания")

    if data.location_id:
        location = await dal_get_location_by_id(data.location_id, db)
        if not location:
            logger.error(f"Location ID {data.location_id} not found")
            raise HTTPException(status_code=404, detail="Адрес не найден")

    if data.type_advertisement_id:
        type_ad = await dal_get_type_advertisement_by_id(data.type_advertisement_id, db)
        if not type_ad:
            logger.error(f"Type advertisement ID {data.type_advertisement_id} not found")
            raise HTTPException(status_code=404, detail="Тип объявления не найден")

    if data.photos and user_role.role_id == 1:
        if not data.photos:
            logger.error("No photos provided for landlord advertisement update")
            raise HTTPException(status_code=400, detail="Требуется хотя бы одна фотография")
        for photo in data.photos:
            if not photo.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                logger.error(f"Invalid file type for photo: {photo.filename}")
                raise HTTPException(status_code=400, detail="Поддерживаются только файлы .png, .jpg, .jpeg")

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        photo_links = []
        for photo in data.photos:
            filename = f"{uuid.uuid4()}.{photo.filename.split('.')[-1]}"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(photo.file, buffer)
            photo_links.append(save_path)
        await dal_update_photos(ad_id, photo_links, db)
    elif data.photos and user_role.role_id != 1:
        logger.error(f"Tenant user {user_id} attempted to update photos for advertisement ID {ad_id}")
        raise HTTPException(status_code=403, detail="Арендаторы не могут обновлять фотографии")

    advertisement = await dal_update_advertisement(
        advertisement_id=ad_id,
        description=data.description,
        number_of_room=data.number_of_room,
        quadrature=data.quadrature,
        floor=data.floor,
        price=data.price,
        number_of_people=data.number_of_people,
        from_the_date=data.from_the_date,
        before_the_date=data.before_the_date,
        location_id=data.location_id,
        type_advertisement_id=data.type_advertisement_id,
        db=db
    )

    logger.info(f"Advertisement ID {ad_id} updated by user_id {user_id}")
    return AdvertisementResponse(message="Объявление успешно обновлено", ad_id=advertisement.id)


async def bll_get_advertisements_by_user(user_id: int, db: AsyncSession) -> List[AdvertisementListResponse]:
    advertisements = await dal_get_advertisements_by_user(user_id, db)
    return await _format_advertisements_response(advertisements, logger)


async def bll_get_landlord_advertisements_for_tenant(user_id: int, db: AsyncSession) -> List[AdvertisementListResponse]:
    user_role = await dal_get_user_role(user_id, 2, db)
    if not user_role:
        logger.error(f"User {user_id} does not have tenant role (role_id=1)")
        raise HTTPException(status_code=403, detail="Доступ разрешен только арендаторам")

    advertisements = await dal_get_advertisements_by_role(1, db)
    return await _format_advertisements_response(advertisements, logger, user_id=user_id)


async def bll_get_tenant_advertisements_for_landlord(user_id: int, db: AsyncSession) -> List[AdvertisementListResponse]:
    user_role = await dal_get_user_role(user_id, 1, db)
    if not user_role:
        logger.error(f"User {user_id} does not have landlord role (role_id=2)")
        raise HTTPException(status_code=403, detail="Доступ разрешен только арендодателям")

    advertisements = await dal_get_advertisements_by_role(2, db)
    return await _format_advertisements_response(advertisements, logger, user_id=user_id)


async def bll_get_advertisement_by_id(ad_id: int, db: AsyncSession) -> AdvertisementListResponse:
    advertisement = await dal_get_adv_by_id(ad_id, db)
    if not advertisement:
        logger.error(f"Advertisement ID {ad_id} not found")
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    
    return (await _format_advertisements_response([advertisement], logger))[0]


async def bll_get_advertisements_by_filter(
    db: AsyncSession,
    type_advertisement_id: Optional[int] = None,
    location_id: Optional[int] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    city_id: Optional[int] = None,
    street_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0
) -> Tuple[List[AdvertisementListResponse], int]:
    if min_price and min_price < 0:
        logger.error(f"Invalid min_price: {min_price}")
        raise HTTPException(status_code=400, detail="Минимальная цена не может быть отрицательной")
    if max_price and max_price < 0:
        logger.error(f"Invalid max_price: {max_price}")
        raise HTTPException(status_code=400, detail="Максимальная цена не может быть отрицательной")
    if min_price and max_price and min_price > max_price:
        logger.error(f"Invalid price range: min_price {min_price} > max_price {max_price}")
        raise HTTPException(status_code=400, detail="Минимальная цена не может быть больше максимальной")
    if from_date and to_date and from_date > to_date:
        logger.error(f"Invalid date range: from {from_date} to {to_date}")
        raise HTTPException(status_code=400, detail="Дата начала должна быть раньше даты окончания")

    advertisements, total = await dal_get_advertisements_by_filter(
        db, type_advertisement_id, location_id, min_price, max_price,
        from_date, to_date, city_id, street_id, limit, offset
    )
    formatted_ads = await _format_advertisements_response(advertisements, logger)
    return formatted_ads, total


async def _format_advertisements_response(advertisements: List[Advertisement], logger, user_id: Optional[int] = None) -> List[AdvertisementListResponse]:
    results = []
    for ad in advertisements:
        user_role_response = None
        if ad.user_role:
            user = ad.user_role.user
            logo_link = user.user_logos[0].logo.logo_link if user.user_logos else None
            user_response = UserResponse(
                id=user.id,
                first_name=user.first_name or "",
                last_name=user.last_name or "",
                surname=user.surname or "",
                phone_number=user.phone_number or "",
                logo_link=logo_link,
            ) if user else None
            role_response = RoleResponse(
                id=ad.user_role.role.id,
                role_name=ad.user_role.role.role_name
            ) if ad.user_role.role else None
            user_role_response = UserRoleResponse(
                id=ad.user_role.id,
                user=user_response,
                role=role_response
            )

        location_response = None
        full_address = None
        if ad.location:
            street_response = StreetsResponse(
                id=ad.location.street.id,
                street_name=ad.location.street.street_name,
                city=CitiesResponse(
                    id=ad.location.street.city.id,
                    city_name=ad.location.street.city.city_name
                )
            ) if ad.location.street else None
            location_response = LocationsResponse(
                id=ad.location.id,
                number=ad.location.number,
                latitude=ad.location.latitude,
                longitude=ad.location.longitude,
                street=street_response
            )
            if ad.location.street and ad.location.street.city:
                full_address = f"г. {ad.location.street.city.city_name}, ул. {ad.location.street.street_name}, д. {ad.location.number}"
            elif ad.location.street:
                full_address = f"ул. {ad.location.street.street_name}, д. {ad.location.number}"
            else:
                full_address = f"д. {ad.location.number}"

        type_ad_response = TypeAdvertisementResponse(
            id=ad.type_advertisement.id,
            type_name=ad.type_advertisement.type_name
        ) if ad.type_advertisement else None

        photo_response = [
            PhotoResponse(id=photo.id, photo_link=photo.photo.photo_link)
            for photo in ad.advertisement_photos
        ]

        is_favourite = False
        if user_id:
            is_favourite = any(fav.user_id == user_id for fav in ad.favorites)

        result = AdvertisementListResponse(
            id=ad.id,
            description=ad.description,
            number_of_room=ad.number_of_room,
            quadrature=ad.quadrature,
            floor=ad.floor,
            price=ad.price,
            number_of_people=ad.number_of_people,
            from_the_date=ad.from_the_date,
            before_the_date=ad.before_the_date,
            location=location_response,
            type_advertisement=type_ad_response,
            user_role=user_role_response,
            photo=photo_response,
            full_address=full_address,
            is_favourite=is_favourite
        )
        results.append(result)
    
    logger.info(f"Formatted {len(results)} advertisements for response, user_id: {user_id}")
    return results


async def bll_delete_advertisement_by_id(ad_id: int, user_id: int, db: AsyncSession) -> AdvertisementResponse:
    advertisement = await dal_get_adv_by_id(ad_id, db)
    if not advertisement:
        logger.error(f"Advertisement ID {ad_id} not found")
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    if advertisement.user_role.user_id != user_id:
        logger.error(f"User {user_id} not authorized to delete advertisement ID {ad_id}")
        raise HTTPException(status_code=403, detail="Доступ запрещен, вы не являетесь владельцем объявления")