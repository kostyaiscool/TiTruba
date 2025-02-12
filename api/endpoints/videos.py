from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse

app = FastAPI()
router = APIRouter()

@router.get('/watch/{vidid}')
async def video_view(vidid: str):
    if vidid == '1':
        played_video = "C:\\Users\\ilyab\\PycharmProjects\\TiTruba\\vidosi\\vid1.webm"
        media_type = "video/webm"
    elif vidid == '2':
        played_video = "C:\\Users\\ilyab\\PycharmProjects\\TiTruba\\vidosi\\vid2.mp4"
        media_type = "video/mp4"
    else:
        return JSONResponse(content={"error": "Invalid video ID"}, status_code=404)

    def video_streamer(played_video):
        with open(played_video, "rb") as video_file:
            while chunk := video_file.read(1024 * 1024):  # Читаем по 1MB
                yield chunk

    return StreamingResponse(video_streamer(played_video), media_type=media_type)


app.include_router(router)
