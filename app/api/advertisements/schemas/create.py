from pydantic import BaseModel
from fastapi import UploadFile
from datetime import date
from typing import List, Optional


class CreateCity(BaseModel):
    city_name: str


class CreateStreet(BaseModel):
    street_name: str
    city_id: int


class CreateLocation(BaseModel):
    number: str
    latitude: float
    longitude: float
    street_id: int


class UserBase(BaseModel):
    first_name: str
    last_name: str
    surname: str
    email: str
    phone_number: str
    role: Optional[str] = None

    class Config:
        from_attributes = True


class TypeCreate(BaseModel):
    type_name: str

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    role_name: str


class UserRoleCreate(BaseModel):
    role_id: int


class CreateAdvertisementByTenant(BaseModel):
    description: str
    number_of_room: int
    quadrature: float
    floor: int
    location_id: Optional[int] = None
    type_advertisement_id: int
    price: int
    from_the_date: date
    before_the_date: date


class CreateAdvertisementByLandlord(BaseModel):
    description: str
    number_of_room: int
    quadrature: float
    floor: int
    price: int
    from_the_date: date
    before_the_date: date
    location_id: int
    type_advertisement_id: int
    photos: List[UploadFile]