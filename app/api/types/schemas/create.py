from pydantic import BaseModel


class TypeCreate(BaseModel):
    type_name: str

    class Config:
        from_attributes=True