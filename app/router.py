from fastapi import APIRouter

from app.api.auth.auth_api import router as auth_router
from app.api.roles.role_api import router as role_router
from app.api.types.type_api import router as type_router
from app.api.users.user_api import router as user_router
from app.api.addresses.address_api import router as address_router
from app.api.nearest_geolocations.nearest_geo_api import router as nearest_geo_router
from app.api.advertisements.advertisement_api import router as advertisement_router
from app.api.favorites.favorite_api import router as favourite_router
from app.api.applications.application_api import router as application_router
from app.api.applications2.application_api import router as application2_router


route=APIRouter()

route.include_router(auth_router, prefix="/auth", tags=["Authentication"])
route.include_router(role_router, prefix="/role", tags=["Role"])
route.include_router(type_router, prefix="/type", tags=["Type"])
route.include_router(user_router, prefix="/user", tags=["User"])
route.include_router(address_router, prefix="/address", tags=["Address"])
route.include_router(nearest_geo_router, prefix="/nearest_geo", tags=["Nearest geolocation"])
route.include_router(advertisement_router, prefix="/adv", tags=["Advertisement"])
route.include_router(favourite_router, prefix="/favorite", tags=["Favorite"])
route.include_router(application_router, prefix="/application", tags=["Application"])

route.include_router(application2_router, prefix="/application2", tags=["Application2"])