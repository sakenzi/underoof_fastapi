from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class AddressResponse(BaseModel):
    message: str


class CitiesResponse(BaseModel):
    id: int
    city_name: str

    class Config:
        from_attributes = True


class StreetsResponse(BaseModel):
    id: int
    street_name: str
    city: Optional[CitiesResponse] = None

    class Config:
        from_attributes = True


class LocationsResponse(BaseModel):
    id: int
    number: str
    latitude: float
    longitude: float
    street: Optional[StreetsResponse] = None

    class Config:
        from_attributes = True


class TypeResponse(BaseModel):
    message: str


class TypeAdvertisementResponse(BaseModel):
    id: int
    type_name: str

    class Config:
        from_attributes = True


class RoleResponse(BaseModel):
    id: int
    role_name: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    surname: str
    phone_number: str

    class Config:
        from_attributes = True


class UserRoleResponse(BaseModel):
    id: int
    user: Optional[UserResponse] = None
    role: Optional[RoleResponse] = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    first_name: str
    last_name: str
    surname: str
    email: str
    phone_number: str
    role: Optional[str] = None

    class Config:
        from_attributes = True


class PhotoResponse(BaseModel):
    id: int
    photo_link: str

    class Config:
        from_attributes = True


class AdvertisementResponse(BaseModel):
    message: str
    ad_id: Optional[int] = None


class AdvertisementListResponse(BaseModel):
    id: int
    description: str
    number_of_room: int
    quadrature: float
    floor: int
    price: int
    number_of_people: Optional[int] = None
    from_the_date: date
    before_the_date: date
    location: Optional[LocationsResponse] = None
    type_advertisement: Optional[TypeAdvertisementResponse] = None
    photo: List[PhotoResponse] = []
    user_role: Optional[UserRoleResponse] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    access_token_expire_time: str
    message: str = "Token generated successfully"
    user: Optional[UserBase] = None