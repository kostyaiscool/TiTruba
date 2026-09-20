from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.auth.models.user import User


class UserCRUD:
    @staticmethod
    async def get_user_by_name(db: AsyncSession, name: str):
        user = await db.execute(select(User).where(User.username == name))
        return user.scalars().one_or_none()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int):
        user = await db.execute(select(User).where(User.id == user_id))
        return user.scalars().one_or_none()

    @staticmethod
    async def has_role(session: AsyncSession, role_name: str, user_id: int) -> bool:
        user = await UserCRUD.get_user_by_id(session, user_id)
        print("Джо Байден упал с лестницы")
        return user.has_role(role_name)

    @staticmethod
    async def has_permission(session: AsyncSession, perm_name: str, user_id: int) -> bool:
        user = await UserCRUD.get_user_by_id(session, user_id)
        for role in user.roles:
            if any(permission.name == perm_name for permission in role.permission):
                return True
        return False