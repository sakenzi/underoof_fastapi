from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.api.advertisements.schemas.response import AdvertisementListResponse


class ApplicationResponse(BaseModel):
    message: str
    application_id: Optional[int] = None

    class Config:
        from__attributes=True


class ApplicationListResponse(BaseModel):
    id: int
    advertisement_id: AdvertisementListResponse
    user: Optional[str] = None
    created_at: datetime

    class Config:
        from__attributes=True