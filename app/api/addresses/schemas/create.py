from pydantic import BaseModel


class CreateCity(BaseModel):
    city_name: str


class CreateStreet(BaseModel):
    street_name: str
    city_id: int


class CreateLocation(BaseModel):
    number: str
    latitue: float
    longitude: float
    street_id: int