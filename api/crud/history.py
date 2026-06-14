from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.users import UserCRUD
from crud.videos import VideoCRUD
from models.history import History


class HistoryCRUD():
    @staticmethod
    async def get_history_by_viewer(
            db: AsyncSession,
            viewer_id: int,
    ):
        history = await db.execute(select(History).where(History.viewer_id == viewer_id))
        return history.scalars().all()

    @staticmethod
    async def add_video_history(
            db: AsyncSession,
            viewer_id: int,
            video_id: int
    ):
        video = await VideoCRUD.get_video(db, video_id)
        user = await UserCRUD.get_user_by_id(db, viewer_id)
        history = History(
            viewer_id=viewer_id,
            video_id=video_id,
            video=video,
            viewer=user
        )

        db.add(history)
        await db.commit()
        await db.refresh(history)

        return history