from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    surname: str
    email: str
    phone_number: str
    role: str