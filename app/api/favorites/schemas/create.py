from pydantic import BaseModel


class FavoriteCreate(BaseModel):
    advertisement_id: int