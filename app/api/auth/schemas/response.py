from pydantic import BaseModel
# from datetime import datetime


class TokenResponse(BaseModel):
    access_token: str
    access_token_expire_time: str
    message: str = "Token generated successfully"