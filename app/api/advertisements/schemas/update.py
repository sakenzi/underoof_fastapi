from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from fastapi import UploadFile


class UpdateAdvertisement(BaseModel):
    description: Optional[str] = None
    number_of_room: Optional[int] = None
    quadrature: Optional[float] = None
    floor: Optional[int] = None
    price: Optional[int] = None
    number_of_people: Optional[int] = None
    from_the_date: Optional[date] = None
    before_the_date: Optional[date] = None
    location_id: Optional[int] = None
    type_advertisement_id: Optional[int] = None
    photos: Optional[List[UploadFile]] = None

    class Config:
        from_attributes = True