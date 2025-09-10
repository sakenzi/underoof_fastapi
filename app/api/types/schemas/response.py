from pydantic import BaseModel
from typing import Optional


class TypeResponse(BaseModel):
    message: str


class TypeBase(BaseModel):
    id: int
    type_name: str


class RoleResponse(BaseModel):
    message: str


class RolesResponse(BaseModel):
    id: int
    role_name: str


class UserBase(BaseModel):
    first_name: str
    last_name: str
    surname: str
    email: str
    phone_number: str
    role: str | None


class TokenResponse(BaseModel):
    access_token: str
    access_token_expire_time: str
    message: str = "Token generated successfully"
    user: Optional[UserBase] = None