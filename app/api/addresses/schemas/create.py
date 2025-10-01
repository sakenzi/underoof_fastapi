from pydantic import BaseModel
from typing import Optional


class CreateCity(BaseModel):
    city_name: str


class CreateStreet(BaseModel):
    street_name: str
    city_id: int


class CreateLocation(BaseModel):
    number: str
    latitude: float
    longitude: float
    street_id: int


class LocationSearchRequest(BaseModel):
    city_name: Optional[str] = None
    street_name: Optional[str] = None
    min_latitude: Optional[float] = None
    max_latitude: Optional[float] = None
    min_longitude: Optional[float] = None
    max_longitude: Optional[float] = None


class StreetSearchRequest(BaseModel):
    street_name: str
    city_name: Optional[str] = None


class AddressSearchRequest(BaseModel):
    query: str