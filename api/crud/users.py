from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.auth.models.user import User


class UserCRUD:
    @staticmethod
    async def get_user_by_name(db: AsyncSession, name: str):
        user = await db.execute(select(User).where(User.username == name))
        return user.scalars().one()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int):
        user = await db.execute(select(User).where(User.id == user_id))
        return user.scalars().one()