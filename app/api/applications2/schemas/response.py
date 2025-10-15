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
    proposed_advertisement: Optional[AdvertisementListResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationTenantListResponse(BaseModel):
    id: int
    advertisement: AdvertisementListResponse
    proposed_advertisement: Optional[AdvertisementListResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationResponseWrapper(BaseModel):
    applications: List[ApplicationListResponse]

    class Config:
        from_attributes = True