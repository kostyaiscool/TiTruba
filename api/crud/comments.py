from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from models.commentaries import Comments
from schemas.commentaries import CommentCreate, Comment


class CommentCRUD():
    @staticmethod
    async def get_comments_from_video(
            db: AsyncSession,
            video_id: int
    ):
        result = await db.execute(
            select(Comments)
            .where(video_id == Comments.video_id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_comment(db: AsyncSession, id: int):
        comment = await db.execute(select(Comments).where(Comments.id == id))
        comment = comment.scalars().one()
        return comment

    @staticmethod
    async def create(session: AsyncSession, comm_data: CommentCreate):
        comment = Comment(**comm_data.dict())
        session.add(comment)

        await session.commit()
        await session.refresh(comment)

        return comment

    @staticmethod
    async def get_comment_with_replies(
            session: AsyncSession,
            parent_id: int
    ):
        try:
            result = await session.execute(select(Comment).where(Comment.parent_id == parent_id))
            return result.scalars().all()
        except NoResultFound:
            return None