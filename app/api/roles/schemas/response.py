from pydantic import BaseModel


class RoleResponse(BaseModel):
    message: str


class RolesResponse(BaseModel):
    role_name: str