from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.security import HTTPBearer
from fastapi_users import BaseUserManager
from fastapi_users.exceptions import UserAlreadyVerified
from starlette.requests import Request

from api.modules.auth.backend import auth_backend
from api.modules.auth.dependencies.user_manager import get_user_manager
from api.modules.auth.routers.fastapi_users_endpoints import fastapi_users_routers
from api.modules.auth.schemas.user import UserCreate, UserRead

http_bearer = HTTPBearer(auto_error=False)

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(http_bearer)],
)

# /login
# /logout
auth_router.include_router(
    router=fastapi_users_routers.get_auth_router(
        auth_backend,
        # requires_verification=True
    ),
)

# /register
auth_router.include_router(
    router=fastapi_users_routers.get_register_router(
        UserRead,
        UserCreate,
    ),
)

# /request-verify-token
@auth_router.post("/request-verify-token")
async def request_verify_token(
    request: Request,
    email: str = Body(..., embed=True),
    user_manager: BaseUserManager = Depends(get_user_manager),
):
    user = await user_manager.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User with this email was not found")
    try:
        await user_manager.request_verify(user, request=request)
    except UserAlreadyVerified:
        return {"detail": "The user is already verified"}
    return {"detail": "Verification link has been sent"}

# /verify
auth_router.include_router(
    router=fastapi_users_routers.get_verify_router(UserRead),
)

# /forgot-password
@auth_router.post("/forgot-password")
async def forgot_password(
    request: Request,
    email: str = Body(..., embed=True),
    user_manager: BaseUserManager = Depends(get_user_manager),
):
    user = await user_manager.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User with this email was not found")
    await user_manager.forgot_password(user, request=request)
    return {"detail": "Password recovery link sent to your email"}

# /reset-password
auth_router.include_router(
    router=fastapi_users_routers.get_reset_password_router(),
)