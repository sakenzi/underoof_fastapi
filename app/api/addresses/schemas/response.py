from pydantic import BaseModel


class CitiesResponse(BaseModel):
    id: int
    city_name: str

    class Config:
        from_attributes=True


class StreetsResponse(BaseModel):
    id: int
    street_name: str

    class Config:
        from_attributes=True


class LocationsResponse(BaseModel):
    id: int
    number: str
    latitude: float
    longitude: float

    class Config:
        from_attributes=True