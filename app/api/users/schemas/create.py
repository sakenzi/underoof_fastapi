from pydantic import BaseModel
from typing import Optional


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


class LogoResponse(BaseModel):
    message: str
    logo_id: int | None = None

    class Config:
        from__attributes=True