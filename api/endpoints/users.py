from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from modules.auth.routers.fastapi_users_endpoints import fastapi_users_routers
from modules.auth.schemas.user import UserRead, UserUpdate

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(http_bearer)])
router.include_router(
    router=fastapi_users_routers.get_users_router(
        UserRead,
        UserUpdate
    )
)