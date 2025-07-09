from pydantic import BaseModel
# from datetime import datetime


class TokenResponse(BaseModel):
    access_token: str
    access_token_expire_time: str


# class MessageResponse(BaseModel):
#     status_code: int | None
#     message: str


# class ResponseMessage(BaseModel):
#     message: str