from pydantic import BaseModel


class PhoneNumberInput(BaseModel):
    phone_number: str


class VerifyPhoneInput(BaseModel):
    phone_number: str
    code: str
    username: str
    password: str