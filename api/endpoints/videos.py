from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse

app = FastAPI()
router = APIRouter()

@router.get('/watch/{vidid}')
async def video_view(vidid: str):
    if vidid == '1':
        played_video = "C:\\Users\\ilyab\\PycharmProjects\\TiTruba\\vidosi\\vid1.webm"
    elif vidid == '2':
        played_video = "C:\\Users\\ilyab\\PycharmProjects\\TiTruba\\vidosi\\vid2.mp4"

    def video_streamer(played_video):
        with open(played_video, "rb") as video_file:

            while chunk := video_file.read(1024 * 1024):
        # Читаем по 1MB
                yield chunk # Возвращаем потоковый ответ
    return StreamingResponse( video_streamer(played_video), media_type="video/mp4" )

app.include_router(router)
