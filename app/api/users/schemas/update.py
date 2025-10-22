from pydantic import BaseModel
from typing import Optional


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    surname: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True