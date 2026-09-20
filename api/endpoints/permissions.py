from functools import wraps
from typing import Callable
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from crud.users import UserCRUD
from db.session import db_helper
from modules.auth.routers.fastapi_users_endpoints import current_optional_user
from modules.auth.schemas.user import UserRead

router = APIRouter()

@router.get("/require/perm/{perm}")
async def require_permission(role: str, user: UserRead = Depends(current_optional_user), session: AsyncSession = Depends(db_helper.get_session)):
    if not user:
        return False
    has_role = await UserCRUD.has_role(session, role, user.id)
    if has_role:
        return True
    else:
        return False

# def require_role(role: str):
#     """
#     Декоратор для перевірки ролі.
#
#     Usage:
#         @require_role("admin")
#         async def on_admin_panel(...):
#             ...
#     """
#
#     def decorator(func: Callable):
#         global result
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             user = None
#             dialog_manager = None
#             print("243238032308")
#             for arg in args:
#                 print(arg)
#                 print("**********************************************************")
#             print(type(args[1]))
#             user_id = args[1].from_user.id
#             async with db_helper.session() as session:
#                 result = await TelegramUserCRUD.has_role(session, role, user_id)
#             print(result)
#             return await func(*args, **kwargs)
#
#         return wrapper
#
#     return decorator
