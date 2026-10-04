from typing import Optional, List

from fastapi import FastAPI, APIRouter, Depends, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from crud.history import HistoryCRUD
from crud.likescrud import LikesCRUD
from crud.users import UserCRUD
from crud.videotagcrud import VideoTagCRUD, VideoTagInterestCRUD
from models.vidosi import Vidos
from modules.auth.models.user import User
from modules.auth.routers.fastapi_users_endpoints import current_active_user, current_optional_user
from modules.auth.schemas.user import UserRead
from crud.videos import VideoCRUD
from db.session import db_helper
from schemas.vidos import VidosCreate

# app = FastAPI()
router = APIRouter()

@router.get("/watch/{vidid}")
async def video_view(
    vidid: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    video = await VideoCRUD.get_video(session, vidid)
    if not video:
        raise HTTPException(
            status_code=404,
            detail="Видео не найдено"
        )

    played_video = video.file_path
    media_type = video.content_type

    def video_streamer(path):
        with open(path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                yield chunk

    return StreamingResponse(
        video_streamer(played_video),
        media_type=media_type,
    )

@router.get('/videos/{page}')
async def videos(page: int, db: AsyncSession = Depends(db_helper.session_getter), user: UserRead = Depends(current_optional_user)):
    if not user:
        videos = await VideoCRUD.get_videos(db, page)
        print("мы в вайне")
    else:
        videos = await VideoCRUD.get_fyp(db, page, user)
    return videos

@router.post("/video_upload")
async def video_upload(
    db: AsyncSession = Depends(db_helper.session_getter),
    current_user: UserRead = Depends(current_active_user),
    video: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    tag_ids: List[int] = Form(default=[]),
):
    author_name = current_user.username

    video = await VideoCRUD.save_video(
        db,
        video,
        title,
        description,
        author_name,
        current_user.id,
        tag_ids,
    )

    return video

@router.get("/video_info/{video_id}")
async def video_info(
    video_id: int,
    db: AsyncSession = Depends(
        db_helper.session_getter
    )
):
    video = await VideoCRUD.get_video(
        db,
        video_id
    )
    if not video:
        raise HTTPException(
            status_code=404,
            detail="Видео не найдено"
        )
    tags = await VideoTagCRUD.get_tags_by_videos(db,video.id)
    print("зумерские зумерочки")
    print(video.views)
    return {
        "id": video.id,
        "title": video.public_name,
        "description": video.desc,
        "author": video.author,
        "views": video.views,
        "created_at": video.created_at,
        "video_tags": tags,
    }

# @router.get("/get_video_by_author/{author}")
# async def get_video_by_author(author: str, session: AsyncSession = Depends(db_helper.get_session)):
#     result = await VideoCRUD.get_video_by_author(author, session)
#     return result
@router.get(
    "/get_video_by_author/{author_id}"
)
async def get_video_by_author(
    author_id: int,
    session: AsyncSession = Depends(
        db_helper.session_getter
    )
):
    result = await VideoCRUD.get_video_by_author(
        author_id,
        session
    )

    return result

# @router.post("/like/{video_id}")
# async def like_video(
#     video_id: int,
#     db: AsyncSession = Depends(...),
#     user: UserRead = Depends(current_active_user)
# ):
#     return await LikesCRUD.rate_video(
#         db,
#         user.id,
#         video_id,
#         True
#     )
class WatchData(BaseModel):
    watched_seconds: float

@router.post("/watched/{video_id}")
async def watched(
    video_id: int,
    data: WatchData,
    db: AsyncSession = Depends(db_helper.session_getter),
    user: UserRead = Depends(current_active_user),
):
    # Получаем видео
    video = await VideoCRUD.get_video(
        db,
        video_id
    )
    if not video:
        raise HTTPException(
            status_code=404,
            detail="Видео не найдено"
        )

    # Длина видео
    video_length = video.length or 0

    # Фактически просмотренное время
    watched_seconds = max(
        0.0,
        data.watched_seconds
    )

    watch_percent = (
        watched_seconds / video.length
        if video.length > 0
        else 0.0
    )

    print(
        "Посмотрено:",
        watched_seconds,
        "секунд"
    )

    print(
        "Процент:",
        watch_percent * 100,
        "%"
    )

    # Увеличиваем просмотры
    video.views += 1

    # Определяем вес интереса
    if watch_percent < 0.10:
        interest_weight = 0

    elif watch_percent < 0.30:
        interest_weight = 0.2

    elif watch_percent < 0.50:
        interest_weight = 0.5

    elif watch_percent < 0.80:
        interest_weight = 1

    elif watch_percent < 0.95:
        interest_weight = 1.5

    else:
        interest_weight = 2

    print(
        "Вес интереса:",
        interest_weight
    )

    # Получаем теги видео
    tags = await VideoTagCRUD.get_tags_by_videos(
        db,
        video_id
    )

    # Обновляем интересы пользователя
    for tag in tags:

        interest = await VideoTagInterestCRUD.get_interest(
            db,
            tag.id,
            user.id
        )

        # Если интереса ещё нет — создаём
        if not interest:
            await VideoTagInterestCRUD.add_interest(
                db,
                tag.id,
                user.id
            )

        # Добавляем рассчитанный вес
        if interest_weight > 0:
            await VideoTagInterestCRUD.change_interest(
                db,
                tag.id,
                user.id,
                interest_weight
            )

    # Добавляем видео в историю
    await HistoryCRUD.add_video_history(
        db,
        user.id,
        video_id,
    )

    await db.commit()

    return {
        "success": True,
        "video_id": video_id,
        "watched_seconds": watched_seconds,
        "video_length": video_length,
        "watch_percent": watch_percent,
        "interest_weight": interest_weight,
    }

@router.get("/search/{search}")
async def search_vidos(
        search: str,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    result = await VideoCRUD.search_video(session, search)
    return result

@router.delete("/delete/{video_id}")
async def delete_vidos(
        video_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    result = await VideoCRUD.delete_vidos(session, video_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Видео не найдено"
        )
    return result

@router.patch('/edit_video/{video_id}')
async def video_edit(
    video_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
    title: Optional[str] = None,
    description: Optional[str] = None
):
    video = await VideoCRUD.edit_video(
        db,
        video_id,
        title,
        description,
    )
    if video is None:
        raise HTTPException(
            status_code=404,
            detail="Видео не найдено"
        )
    return video