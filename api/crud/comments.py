from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from models.commentaries import Comments
from schemas.commentaries import CommentCreate


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
        comment = Comments(
            text=comm_data.text,
            video_id=comm_data.video_id,
            parent_id=comm_data.reply_to_id,
            author=comm_data.author.username,
            author_id=comm_data.author.id,
        )
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
            result = await session.execute(select(Comments).where(Comments.parent_id == parent_id))
            return result.scalars().all()
        except NoResultFound:
            return None