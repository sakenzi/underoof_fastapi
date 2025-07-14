from pydantic import BaseModel
from datetime import date
from typing import List


class CreateAdvertisementByLessee(BaseModel):
    description: str
    number_of_room: int
    quadrature: float
    floor: int
    location_id: int
    type_advertisement_id: int
    price: int
    from_the_date: date
    before_the_date: date


class CreateAdvertisementBySeller(BaseModel):
    description: str
    number_of_room: int
    quadrature: float
    floor: int
    price: int
    from_the_date: date
    before_the_date: date
    location_id: int
    type_advertisement_id: int
    photos: List[str]
