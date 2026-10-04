from typing import List, Optional

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from models.roles import Role
from schemas.roles import RoleCreate


class RoleCRUD:
    @staticmethod
    async def get_role(session: AsyncSession, role_id: int) -> Optional[Role]:
        result = await session.execute(select(Role).where(Role.id == role_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_or_update(session: AsyncSession, role_data: RoleCreate) -> Role:
        # Попробуем найти по name (или другому уникальному полю)
        result = await session.execute(
            select(Role).where(Role.name == role_data.name)
        )
        role = result.scalar_one_or_none()
        if role:
            for key, value in role_data.model_dump().items():
                setattr(role, key, value)
        else:
            role = Role(**role_data.model_dump())
            session.add(role)

        await session.commit()
        await session.refresh(role)

        return role

    @staticmethod
    async def get_all_roles(session: AsyncSession) -> List[Role]:
        result = await session.execute(
            select(Role).order_by(desc(Role.id))  # новые первыми
        )
        return list(result.scalars().all())
