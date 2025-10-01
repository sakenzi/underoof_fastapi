from pydantic import BaseModel
from app.api.advertisements.schemas.response import AdvertisementListResponse


class FavoriteResponse(BaseModel):
    favorite_id: int
    user_id: int
    advertisement_id: int
    message: str


class FavoriteListResponse(BaseModel):
    favorite_id: int
    advertisement: AdvertisementListResponse

    class Config:
        from_attributes = True