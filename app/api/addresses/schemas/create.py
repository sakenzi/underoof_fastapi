from pydantic import BaseModel
from typing import Optional

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