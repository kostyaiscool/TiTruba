from typing import Optional

from fastapi import FastAPI, APIRouter, Depends, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from crud.history import HistoryCRUD
from crud.likescrud import LikesCRUD
from crud.users import UserCRUD
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
async def videos(page: int, db: AsyncSession = Depends(db_helper.session_getter)):
    videos = await VideoCRUD.get_videos(db, page)
    return videos

@router.post('/video_upload')
async def video_upload(
    db: AsyncSession = Depends(db_helper.session_getter),
    current_user: UserRead = Depends(current_active_user),
    video: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...)
):
    author_name = current_user.username
    print(current_user)
    print(author_name)
    video = await VideoCRUD.save_video(
        db,
        video,
        title,
        description,
        author_name
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
    print("зумерские зумерочки")
    print(video.views)
    return {
        "id": video.id,
        "title": video.public_name,
        "description": video.desc,
        "author": video.author,
        "views": video.views,
        "created_at": video.created_at,
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
        db_helper.get_session
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

@router.post("/watched/{video_id}")
async def watched(
    video_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
    user: UserRead = Depends(current_active_user),
):
    print("watched")
    print(user)
    video = await VideoCRUD.get_video(
        db,
        video_id
    )

    video.views += 1

    await HistoryCRUD.add_video_history(
        db,
        user.id,
        video_id,
    )

    await db.commit()

    return {
        "success": True
    }