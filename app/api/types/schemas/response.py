from pydantic import BaseModel


class TypeResponse(BaseModel):
    message: str


class TypeBase(BaseModel):
    id: int
    type_name: str