from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse

from configs import VIDEO_PATH

app = FastAPI()
router = APIRouter()


# @router.get('/watch/{vidid}')
# async def video_view(vidid: str):
#     played_video = VIDEO_PATH + '\\' + vidid
#     return FileResponse(played_video, media_type="video/webm", filename="video.webm")
@router.get('/watch/{vidid}')
async def video_view(vidid: str):
    played_video = VIDEO_PATH + '\\' + vidid

    def iterfile():
        with open(played_video, mode="rb") as file:
            yield from file

    return StreamingResponse(iterfile(), media_type="video/webm")

app.include_router(router)
