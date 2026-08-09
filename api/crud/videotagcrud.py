from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import VideoTag, Tag
from models.vidosi import Vidos


class VideoTagCRUD():
    @staticmethod
    async def get_tag(db: AsyncSession, id: int):
        videotag = await db.execute(select(VideoTag).where(VideoTag.id == id))
        videotag = videotag.scalars().one()
        return videotag


    @staticmethod
    async def get_tag_videos(
            db: AsyncSession,
            tag_id: int
    ):
        # tag = await VideoTagCRUD.get_tag(db, tag_id)
        result = await db.execute(
            select(VideoTag).where(VideoTag.video_id==tag_id)
        )
        result2=result.scalars().all()
        print(result2)
        print(tag_id)
        videos = []
        for res in result2:
            video = await db.execute(select(Vidos).where(Vidos.id==res.video_id))
            video = video.scalars().one()
            print(video)
            print(res.video_id)
            print("епоеоркгкггк")
            videos.append(video)
        return videos


    @staticmethod
    async def add_tag(
        session: AsyncSession,
        tag_id: int,
        video_id: int
    ):
        tag = VideoTag(
            video_id=video_id,
            tag_id=tag_id,
            # video=Vidos,
            # tag
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
        tag = await VideoTagCRUD.get_tag(session, tag_id)

        if tag is None:
            return None

        await session.delete(tag)
        await session.commit()