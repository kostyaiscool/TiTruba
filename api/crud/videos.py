import datetime
import time
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile, Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from crud.users import UserCRUD
from db.session import db_helper
from models.history import History
from models.vidosi import Vidos
from modules.auth.models.user import User
from schemas.vidos import VidosCreate

VIDEO_DIR = Path("media/videos")
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

class VideoCRUD():
    @staticmethod
    async def get_videos(
            db: AsyncSession,
            page: int,
            per_page: int = 24,
    ):
        offset = (page - 1) * per_page

        result = await db.execute(
            select(Vidos)
            .order_by(Vidos.created_at.desc())
            .offset(offset)
            .limit(per_page)
        )

        return result.scalars().all()

    @staticmethod
    async def get_video(db: AsyncSession, id: int):
        video = await db.execute(select(Vidos).where(Vidos.id == id))
        video = video.scalars().one()
        await db.commit()
        return video

    # @staticmethod
    # async def create(db: AsyncSession, video_data: VidosCreate):
    #     video = Vidos(**video_data.model_dump())
    #     db.add(video)
    #     await db.commit()
    #     await db.refresh(video)
    #     return video
    @staticmethod
    async def save_video(
            session: AsyncSession,
            file: UploadFile,
            title: str,
            description: str,
            author: str
    ) -> Vidos:
        extension = Path(file.filename).suffix
        unique_name = f"{uuid4()}{extension}"

        file_path = VIDEO_DIR / unique_name

        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)
        video = Vidos(
            name=unique_name,
            public_name=title,
            desc=description,
            file_path=str(file_path),
            file_size=len(content),
            content_type=file.content_type,
            author=author
        )

        session.add(video)
        await session.commit()
        await session.refresh(video)

        return video
    # @staticmethod
    # async def get_video_by_author(authora: str, session: AsyncSession):
    #     # author = await session.execute(select(User).where(User.id == authora))
    #     # authore = author.scalars().one()
    #     video = await session.execute(select(Vidos).where(Vidos.author == authora))
    #     return video.scalars().all()
    from sqlalchemy import select

    from sqlalchemy import select

    @staticmethod
    async def get_video_by_author(
            author_id: int,
            session: AsyncSession,
    ):
        print(User)
        # user_result = await session.execute(
        #     select(User).where(
        #         User.id == author_id
        #     )
        # )
        #
        # user = user_result.scalars().one()
        user = await UserCRUD.get_user_by_id(session, author_id)
        print(user)
        videos_result = await session.execute(
            select(Vidos).where(
                Vidos.author == user.username
            )
        )
        videos = videos_result.scalars().all()
        print(videos)
        return videos

    @staticmethod
    async def add_history(session, user_id, video_id):
        history = History(
            viewer_id=user_id,
            video_id=video_id,
        )
        result = await session.add(history)
        session.commit()
        return result