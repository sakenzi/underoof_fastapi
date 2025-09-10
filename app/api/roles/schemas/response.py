from pydantic import BaseModel

class RoleResponse(BaseModel):
    message: str

class RolesResponse(BaseModel):
    id: int
    role_name: str