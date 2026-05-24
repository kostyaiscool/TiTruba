from fastapi import FastAPI, APIRouter, Depends, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.pickleable import User
from starlette.responses import StreamingResponse

from models.vidosi import Vidos
from modules.auth.routers.fastapi_users_endpoints import current_active_user
from modules.auth.schemas.user import UserRead
from crud.videos import VideoCRUD
from db.session import db_helper
from schemas.vidos import VidosCreate

# app = FastAPI()
router = APIRouter()

@router.get('/watch/{vidid}')
async def video_view(vidid: int, session: AsyncSession = Depends(db_helper.session_getter)):
    # if vidid == '1':
    #     played_video = "C:\\Users\\ilyab\\PycharmProjects\\TiTruba\\vidosi\\vid1.webm"
    #     media_type = "video/webm"
    # elif vidid == '2':
    #     played_video = "C:\\Users\\ilyab\\PycharmProjects\\TiTruba\\vidosi\\vid2.mp4"
    #     media_type = "video/mp4"
    # else:
    #     return JSONResponse(content={"error": "Invalid video ID"}, status_code=404)
    video = await VideoCRUD.get_video(session, vidid)
    played_video = video.file_path
    media_type = video.content_type

    def video_streamer(played_video):
        with open(played_video, "rb") as video_file:
            while chunk := video_file.read(1024 * 1024):  # Читаем по 1MB
                yield chunk

    return StreamingResponse(video_streamer(played_video), media_type=media_type)

@router.get('/videos')
async def videos(db: AsyncSession = Depends(db_helper.session_getter)):
    videos = await VideoCRUD.get_videos(db)
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
    video = await VideoCRUD.save_video(
        db,
        video,
        title,
        description,
        author_name
    )
    return video

@router.get("/info/{video_id}")
async def get_video_info(
    video_id: int,
    db: AsyncSession = Depends(
        db_helper.session_getter
    ),
):
    video = await db.get(Vidos, video_id)

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    return {
        "id": video.id,
        "author": video.author,
        "public_name": video.public_name,
        "desc": video.desc,
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