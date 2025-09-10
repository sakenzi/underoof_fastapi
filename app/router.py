from fastapi import APIRouter
from app.api.auth.auth_api import router as auth_router
from app.api.roles.role_api import router as role_router
from app.api.types.type_api import router as type_router
from app.api.users.user_api import router as user_router

route=APIRouter()

route.include_router(auth_router, prefix="/auth", tags=["Authentication"])
route.include_router(role_router, prefix="/role", tags=["Role"])
route.include_router(type_router, prefix="/type", tags=["Type"])
route.include_router(user_router, prefix="/user", tags=["User"])