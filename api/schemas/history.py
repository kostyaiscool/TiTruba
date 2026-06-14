from pydantic import BaseModel


class Vidos(BaseModel):
    viewer_id: int
    video_id: int
    viewer: User