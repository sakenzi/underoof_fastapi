from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.advertisements.schemas.response import AdvertisementListResponse
from app.api.addresses.schemas.response import (
    LocationsResponse, 
    StreetsResponse, 
    CitiesResponse,
)
from app.api.advertisements.schemas.response import (
    UserResponse, 
    RoleResponse, 
    UserRoleResponse, 
    PhotoResponse, 
    TypeAdvertisementResponse,
)
from app.api.nearest_geolocations.crud.nearest_geo_crud import dal_get_nearest_geolocations
import logging
from typing import List


logger = logging.getLogger(__name__)

async def bll_get_nearest_geolocations(latitude: float, longitude: float, radius: float, db: AsyncSession) -> List[AdvertisementListResponse]:
    if not -90 <= latitude <= 90:
        logger.error(f"Invalid latitude: {latitude}")
        raise HTTPException(status_code=400, detail="Широта должна быть между -90 и 90")
    if not -180 <= longitude <= 180:
        logger.error(f"Invalid longitude: {longitude}")
        raise HTTPException(status_code=400, detail="Долгота должна быть между -180 и 180")
    if radius <= 0:
        logger.error(f"Invalid radius: {radius}")
        raise HTTPException(status_code=400, detail="Радиус должен быть положительным")

    advertisements = await dal_get_nearest_geolocations(latitude, longitude, radius, db)
    
    results = []
    for ad in advertisements:
        user_role_response = None
        if ad.user_role:
            user = ad.user_role.user
            user_response = UserResponse(
                id=user.id,
                first_name=user.first_name or "",
                last_name=user.last_name or "",
                surname=user.surname or "",
                phone_number=user.phone_number or ""
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

        result = AdvertisementListResponse(
            id=ad.id,
            description=ad.description,
            number_of_room=ad.number_of_room,
            quadrature=ad.quadrature,
            floor=ad.floor,
            price=ad.price,
            from_the_date=ad.from_the_date,
            before_the_date=ad.before_the_date,
            location=location_response,
            type_advertisement=TypeAdvertisementResponse(
                id=ad.type_advertisement.id,
                type_name=ad.type_advertisement.type_name
            ) if ad.type_advertisement else None,
            user_role=user_role_response,
            photo=[PhotoResponse(id=photo.id, photo_link=photo.photo.photo_link) for photo in ad.advertisement_photos]
        )
        results.append(result)
    
    logger.info(f"Formatted {len(results)} advertisements for response")
    return results