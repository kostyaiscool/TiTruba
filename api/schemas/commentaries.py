from typing import Optional

from pydantic import BaseModel, DirectoryPath, PastDatetime

from modules.auth.schemas.user import UserRead


class Comment(BaseModel):
    id: int
    text: str
    video_id: int
    length: int
    date: PastDatetime
    author: UserRead
    author_id: int
    reply_to_id: Optional[int]

class CommentCreate(BaseModel):
    text: str
    video_id: int
    reply_to_id: Optional[int]
    author: UserRead