import datetime
import os
import time
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile, Depends
from sqlalchemy import select, desc, delete, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Optional

from crud.users import UserCRUD
from db.session import db_helper
from models.history import History
from models.vidosi import Vidos
from modules.auth.models.user import User
import schemas.vidos

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

    # @staticmethod
    # async def search_video(session: AsyncSession, video_name: str) -> List[Vidos]:
    #         print(video_name)
    #         query = select(Vidos).where(
    #             Vidos.public_name.ilike(f"%{video_name}%")
    #         )
    #         result = await session.execute(query)
    #         finalresult = result.scalars().all()
    #         print(finalresult)
    #         return finalresult

    @staticmethod
    async def search_video(
            session: AsyncSession,
            video_name: str
    ) -> List[Vidos]:
        result = await session.execute(
            select(Vidos).where(
                Vidos.public_name.ilike(f"%{video_name}%")
            )
        )

        return list(result.scalars().all())

    # @staticmethod
    # async def delete_vidos(
    #         session: AsyncSession,
    #         video_id: int,
    # ):
    #     video = await VideoCRUD.get_video(session, video_id)
    #     video_l = Union[video]
    #     result = await session.execute(delete(video_l))
    #     await session.commit()
    #     os.remove(video.file_path)
    #     return result
    @staticmethod
    async def delete_vidos(
            session: AsyncSession,
            video_id: int,
    ):
        video = await VideoCRUD.get_video(session, video_id)

        if video is None:
            return None

        await session.delete(video)
        await session.commit()

        if os.path.exists(video.file_path):
            os.remove(video.file_path)

        return True

    @staticmethod
    async def edit_video(
            session: AsyncSession,
            video_id: int,
            title: Optional[str],
            description: Optional[str],
    ):
        video = await VideoCRUD.get_video(session, video_id)

        if video is None:
            return None

        if title is not None:
            video.public_name = title

        if description is not None:
            video.desc = description

        await session.commit()
        await session.refresh(video)

        return video