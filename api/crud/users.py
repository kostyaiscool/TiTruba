from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Permission, Role, RolePermission, UserRole
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
        # отдельным запросом: ленивая загрузка user.user_roles в async-сессии падает
        result = await session.execute(
            select(UserRole.id)
            .join(Role, Role.id == UserRole.role_id)
            .where(
                UserRole.user_id == user_id,
                Role.name == role_name,
            )
            .limit(1)
        )
        return result.first() is not None

    @staticmethod
    async def has_permission(session: AsyncSession, perm_name: str, user_id: int) -> bool:
        result = await session.execute(
            select(UserRole.id)
            .join(RolePermission, RolePermission.role_id == UserRole.role_id)
            .join(Permission, Permission.id == RolePermission.permission_id)
            .where(
                UserRole.user_id == user_id,
                Permission.name == perm_name,
            )
            .limit(1)
        )
        return result.first() is not None
