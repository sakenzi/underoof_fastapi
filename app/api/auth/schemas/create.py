from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class EmailRequest(BaseModel):
    email: EmailStr = Field(..., max_length=100)


class UserCreate(BaseModel):
    first_name: Optional[str] = Field("", max_length=100)
    last_name: Optional[str] = Field("", max_length=100)
    surname: Optional[str] = Field("", max_length=100) 
    email: EmailStr = Field(..., max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    password: str = Field(..., min_length=8) 


class UserLogin(BaseModel):
    email: EmailStr = Field(..., max_length=50)
    password: str = Field(..., min_length=8) 


class VerifyEmail(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)
