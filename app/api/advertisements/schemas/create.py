from pydantic import BaseModel
from datetime import date


class CreateAdvertisementByLessee(BaseModel):
    description: str
    nymber_of_room: int
    quadrature: float
    floor: int
    location_id: int
    type_advertisement_id: int
    price: int
    from_the_date: date
    before_the_date: date