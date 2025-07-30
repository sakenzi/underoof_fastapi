from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# class PhoneNumberInput(BaseModel):
#     phone_number: str


# class VerifyPhoneInput(BaseModel):
#     phone_number: str
#     code: str
#     username: str
#     password: str


# class UserLogin(BaseModel):
#     phone_number: str
#     password: str


# class UserRegister(BaseModel):
#     phone_number: str
#     username: str
#     password: str

class EmailRequest(BaseModel):
    email: EmailStr = Field(..., max_length=100)


class UserCreate(BaseModel):
    username: Optional[str] = Field("", max_length=100)
    email: EmailStr = Field(..., max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    password: str = Field(..., min_length=8) 


class UserLogin(BaseModel):
    email: EmailStr = Field(..., max_length=50)
    password: str = Field(..., min_length=8) 


class VerifyEmail(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)
