from pydantic import BaseModel


class RoleResponse(BaseModel):
    message: str