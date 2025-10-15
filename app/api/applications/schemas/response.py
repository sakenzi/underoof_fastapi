from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.api.advertisements.schemas.response import AdvertisementListResponse, UserResponse


class ApplicationResponse(BaseModel):
    message: str
    application_id: Optional[int] = None

    class Config:
        from_attributes = True


class ApplicationListResponse(BaseModel):
    id: int
    advertisement: AdvertisementListResponse
    user: Optional[UserResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationTenantListResponse(BaseModel):
    id: int
    advertisement: AdvertisementListResponse
    created_at: datetime

    class Config:
        from_attributes = True