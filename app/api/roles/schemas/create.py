from pydantic import BaseModel


class RoleCreate(BaseModel):
    role_name: str


class UserRoleCreate(BaseModel):
    role_id: int