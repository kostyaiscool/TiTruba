from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from crud.users import UserCRUD
from db.session import db_helper
from modules.auth.routers.fastapi_users_endpoints import current_optional_user
from modules.auth.schemas.user import UserRead

router = APIRouter()

@router.get("/require/role/{role}")
async def require_role(role: str, user: UserRead = Depends(current_optional_user), session: AsyncSession = Depends(db_helper.session_getter)):
    if not user:
        return False
    return await UserCRUD.has_role(session, role, user.id)

@router.get("/require/perm/{perm}")
async def require_permission(perm: str, user: UserRead = Depends(current_optional_user), session: AsyncSession = Depends(db_helper.session_getter)):
    if not user:
        return False
    return await UserCRUD.has_permission(session, perm, user.id)
