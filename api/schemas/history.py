from pydantic import BaseModel

from modules.auth.schemas.user import UserRead


class Vidos(BaseModel):
    viewer_id: int
    video_id: int
    viewer: UserRead
