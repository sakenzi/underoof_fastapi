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