from pydantic import BaseModel, Field
from typing import Optional


class PhoneVerifyRequest(BaseModel):
    phone: str = Field(..., max_length=20, pattern=r"^\+?\d{10,15}$")


class PhoneVerifyCode(BaseModel):
    phone: str = Field(..., max_length=20)
    code: str = Field(..., min_length=6, max_length=6)