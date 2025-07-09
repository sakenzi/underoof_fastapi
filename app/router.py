from fastapi import APIRouter
from app.api.auth.auth_api import router as auth_router


route = APIRouter()

route.include_router(auth_router, prefix='/auth', tags=["USER_AUTHENTICATION"])