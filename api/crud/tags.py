from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Tag


class TagCRUD():
    # @staticmethod
    # async def get_tags(
    #         db: AsyncSession,
    # ):
    #     result = await db.execute(
    #         select(Tag)
    #     )
    #     return result.scalars().all()

    @staticmethod
    async def get_tag(db: AsyncSession, id: int):
        tag = await db.execute(select(Tag).where(Tag.id == id))
        tag = tag.scalars().one()
        return tag

    @staticmethod
    async def add_tag(
        session: AsyncSession,
        tag_name: str
    ):
        tag = Tag(
            name=tag_name,
        )

        session.add(tag)
        await session.commit()
        await session.refresh(tag)

        return tag

    @staticmethod
    async def remove_tag(
        session: AsyncSession,
        tag_id: int
    ):
        tag = await TagCRUD.get_tag(session, tag_id)

        if tag is None:
            return None

        await session.delete(tag)
        await session.commit()