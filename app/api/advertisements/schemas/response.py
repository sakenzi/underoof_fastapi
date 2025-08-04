from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List


class UserResponse(BaseModel):
    id: int
    username: str
    phone_number: str

    class Config:
        from_attributes=True


class RoleResponse(BaseModel):
    id: int
    role_name: str

    class Config:
        from_attributes=True


class UserRoleResponse(BaseModel):
    id: int
    user: Optional[UserResponse]
    role: Optional[RoleResponse]

    class Config:
        from_attributes=True


class CityResponse(BaseModel):
    id: int
    city_name: str

    class Config:
        from_attributes=True


class StreetResponse(BaseModel):
    id: int
    street_name: str
    city: Optional[CityResponse]

    class Config:
        from_attributes=True


class LocationResponse(BaseModel):
    id: int
    number: str
    latitude: float
    longitude: float
    street: Optional[StreetResponse]

    class Config:
        from_attributes=True


class TypeAdvertisementResponse(BaseModel):
    id: int
    type_name: str

    class Config:
        from_attributes=True


class PhotoResponse(BaseModel):
    id: int
    photo_link: str

    class Config:
        from_attributes=True


class AdvertisementResponse(BaseModel):
    id: int
    description: str
    number_of_room: int
    quadrature: float
    floor: int
    price: int
    from_the_date: date
    before_the_date: date
    location: Optional[LocationResponse]
    type_advertisement: Optional[TypeAdvertisementResponse]
    photo: List[PhotoResponse] = []
    user_role: UserRoleResponse


    class Config:
        from_attributes=True

    
class AdvertisementsResponse(BaseModel):
    id: int
    description: str
    number_of_room: int
    quadrature: float
    floor: int
    price: int
    from_the_date: date
    before_the_date: date
    type_advertisement_id: int
    location_id: int
    photo: List[PhotoResponse] = []

    class Config:
        from_attributes = True