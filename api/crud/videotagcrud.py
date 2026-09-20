from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.videos import VideoCRUD
from models import VideoTag, Tag
from models.usertaginterest import UserTagInterest
from models.vidosi import Vidos


class VideoTagCRUD():
    @staticmethod
    async def get_tags(
            db: AsyncSession,
    ):
        result = await db.execute(
            select(VideoTag)
        )
        return result.scalars().all()

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
        result = await db.execute(
            select(Vidos)
            .join(VideoTag, VideoTag.video_id == Vidos.id)
            .where(VideoTag.tag_id == tag_id)
        )
        videos = result.scalars().all()
        return videos
        # print(result2)
        # print(tag_id)
        # videos = []
        # for res in result2:
        #     video = await db.execute(select(Vidos).where(Vidos.id==res.video_id))
        #     video = video.scalars().one()
        #     print(video)
        #     print(res.video_id)
        #     print("епоеоркгкггк")
        #     videos.append(video)
        # return videos

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

    @staticmethod
    async def get_tags_by_videos(
            db: AsyncSession,
            vid_id: int
    ):
        result = await db.execute(
            select(Tag)
            .join(VideoTag, VideoTag.tag_id == Tag.id)
            .where(VideoTag.video_id == vid_id)
        )

        return result.scalars().all()


class VideoTagInterestCRUD():
    @staticmethod
    async def get_interest(db: AsyncSession, tag_id: int, user_id: int):
        interest = await db.execute(select(UserTagInterest).where(UserTagInterest.user_id == user_id,
                                                                           UserTagInterest.tag_id == tag_id))
        interest = interest.scalars().one_or_none()
        return interest

    # @staticmethod
    # async def check_interest(db: AsyncSession, tag_id: int, user_id: int):
    #     user_tag_interest = await VideoTagInterestCRUD.get_interest(db, tag_id, user_id)
    #     if user_tag_interest:
    #

    @staticmethod
    async def change_interest(db: AsyncSession, tag_id: int, user_id: int, change: float):
        user_tag_interest = await VideoTagInterestCRUD.get_interest(db, tag_id, user_id)
        print(user_tag_interest.weight)
        print('а шо если')
        user_tag_interest.weight += change
        print(user_tag_interest.weight)

    @staticmethod
    async def add_interest(session: AsyncSession, tag_id: int, user_id: int):
        interest = UserTagInterest(
            user_id=user_id,
            tag_id=tag_id,
            weight=0,
        )
        session.add(interest)
        await session.commit()
        await session.refresh(interest)

        return interest
