from fastapi import APIRouter
from app.api.auth.auth_api import router as auth_router
from app.api.roles.role_api import router as role_router
from app.api.addresses.address_api import router as address_router
from app.api.types.type_api import router as type_router
from app.api.advertisements.advertisement_api import router as advertisement_router


route = APIRouter()

route.include_router(auth_router, prefix='/auth', tags=["USER_AUTHENTICATION"])
route.include_router(role_router, prefix='/role', tags=["ROLE"])
route.include_router(address_router, prefix='/address', tags=["ADDRESS"])
route.include_router(type_router, prefix='/type', tags=["TYPE"])
route.include_router(advertisement_router, prefix='/advertisement', tags=["ADVERTISEMENT"])