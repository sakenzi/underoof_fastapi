from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    surname: str
    email: str
    phone_number: str
    role: str

class TokenResponse(BaseModel):
    access_token: str
    access_token_expire_time: str
    message: str = "Token generated successfully"
    user: UserBase

