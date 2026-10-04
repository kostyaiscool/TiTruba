import datetime
import os
import random
import time
from pathlib import Path
from uuid import uuid4

import ffmpeg
from fastapi import UploadFile, Depends
from sqlalchemy import select, desc, delete, Sequence, case, exists, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Optional

from crud.users import UserCRUD
from db.session import db_helper
from models import VideoTag, Tag
from models.history import History
from models.usertaginterest import UserTagInterest
from models.vidosi import Vidos
from modules.auth.models.user import User
import schemas.vidos
from modules.auth.schemas.user import UserRead

os.environ["PATH"] += os.pathsep + r"C:\Users\ilyab\AppData\Local\ffmpegio\ffmpeg-downloader\ffmpeg\bin"


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
        video = video.scalars().one_or_none()
        return video

    # @staticmethod
    # async def create(db: AsyncSession, video_data: VidosCreate):
    #     video = Vidos(**video_data.model_dump())
    #     db.add(video)
    #     await db.commit()
    #     await db.refresh(video)
    #     return video
    @staticmethod
    async def get_video_duration(file_path):
        probe = ffmpeg.probe(file_path)

        return int(float(
            probe["format"]["duration"]
        ))

    from sqlalchemy import select

    @staticmethod
    async def save_video(
            session: AsyncSession,
            file: UploadFile,
            title: str,
            description: str,
            author: str,
            author_id: int,
            tag_ids: List[int],
    ) -> Vidos:

        extension = Path(file.filename).suffix
        unique_name = f"{uuid4()}{extension}"
        file_path = VIDEO_DIR / unique_name

        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)

        duration = await VideoCRUD.get_video_duration(str(file_path))

        video = Vidos(
            name=unique_name,
            public_name=title,
            desc=description,
            file_path=str(file_path),
            file_size=len(content),
            content_type=file.content_type,
            author=author,
            author_id=author_id,
            length=duration,
        )

        session.add(video)
        await session.flush()

        # --------------------------------
        # Автоматический поиск тегов
        # --------------------------------

        text = f"{title} {description}".lower()

        result = await session.execute(
            select(Tag)
        )

        all_tags = result.scalars().all()

        for tag in all_tags:

            tag_name = tag.name.lower()

            # Ищем название тега в тексте
            if tag_name in text:
                tag_ids.append(tag.id)

        # Убираем дубли
        tag_ids = list(dict.fromkeys(tag_ids))

        # Максимум 5 тегов
        tag_ids = tag_ids[:5]

        for tag_id in tag_ids:
            session.add(
                VideoTag(
                    video_id=video.id,
                    tag_id=tag_id,
                )
            )

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
        session.add(history)
        await session.commit()
        return history

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

    # @staticmethod
    # async def get_fyp(
    #         db: AsyncSession,
    #         page: int,
    #         user: UserRead,
    #         per_page: int = 24,
    # ):
    #     offset = (page - 1) * per_page
    #     interest = await db.execute(select(UserTagInterest).where(UserTagInterest.user_id==user.id))
    #     interest = interest.scalars().all()
    #     tags = []
    #     for i in interest:
    #         print(i, interest)
    #         print("а ты видел в тт темный друн?")
    #         tag = i.tag_id
    #         tags.append(tag)
    #     # result = await db.execute(
    #     #     select(Vidos)
    #     #     .order_by(Vidos.created_at.desc())
    #     #     .offset(offset)
    #     #     .limit(per_page)
    #     # )
    #     #
    #     videos = await db.execute(
    #         select(Vidos)
    #         .join(VideoTag)
    #         # .where()
    #         .order_by(Vidos.created_at.desc(), VideoTag.tag_id.in_(tags).desc())
    #         .offset(offset)
    #         .limit(per_page)
    #     )
    #     return videos.scalars().all()
    from sqlalchemy import select, case, exists

    @staticmethod
    async def get_fyp(
            db: AsyncSession,
            page: int,
            user: UserRead,
            per_page: int = 24,
    ):
        offset = (page - 1) * per_page
        result = await db.execute(
            select(UserTagInterest.tag_id)
            .where(
                UserTagInterest.user_id == user.id
            )
        )
        tags = result.scalars().all()
        if not tags:
            result = await db.execute(
                select(Vidos)
                .order_by(
                    Vidos.created_at.desc()
                )
                .offset(offset)
                .limit(per_page)
            )
            return result.scalars().all()
        has_interesting_tag = exists(
            select(VideoTag.id)
            .where(
                VideoTag.video_id == Vidos.id,
                VideoTag.tag_id.in_(tags)
            )
        )
        priority = case(
            (has_interesting_tag, 1),
            else_=0
        )
        result = await db.execute(
            select(Vidos)
            .order_by(priority.desc(), Vidos.created_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        videos = list(result.scalars().all())
        random_count = round(len(videos) * 0.1)

        if random_count:
            random_result = await db.execute(
                select(Vidos)
                .order_by(func.random())
                .limit(random_count)
            )

            random_videos = random_result.scalars().all()

            positions = random.sample(
                range(len(videos)),
                min(random_count, len(videos))
            )

            for pos, random_video in zip(positions, random_videos):
                videos[pos] = random_video

        return videos