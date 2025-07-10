from fastapi import APIRouter
from app.api.auth.auth_api import router as auth_router
from app.api.roles.role_api import router as role_router


route = APIRouter()

route.include_router(auth_router, prefix='/auth', tags=["USER_AUTHENTICATION"])
route.include_router(role_router, prefix='/role', tags=["ROLE"])