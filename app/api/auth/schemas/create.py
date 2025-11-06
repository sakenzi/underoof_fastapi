from pydantic import (
    BaseModel, 
    EmailStr, 
    Field, 
    field_validator, 
    ValidationInfo,
)
from typing import Optional


class EmailRequest(BaseModel):
    email: EmailStr = Field(..., max_length=100)


class UserCreate(BaseModel):
    first_name: Optional[str] = Field("", max_length=100)
    last_name: Optional[str] = Field("", max_length=100)
    surname: Optional[str] = Field("", max_length=100) 
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: str = Field(..., min_length=8) 

    @field_validator("email", "phone_number")
    @classmethod
    def check_email_or_phone(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        values = info.data
        if info.field_name == "email" and not v and not values.get("phone_number"):
            raise ValueError("Необходимо указать email или номер телефона")
        if info.field_name == "phone_number" and not v and not values.get("email"):
            raise ValueError("Необходимо указать email или номер телефона")
        return v


class UserLogin(BaseModel):
    email: EmailStr = Field(..., max_length=50)
    password: str = Field(..., min_length=8) 


class UserLoginBase(BaseModel):
    login: str = Field(..., max_length=100, description="Email или номер телефона")
    password: str = Field(..., min_length=8)


class VerifyEmail(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)