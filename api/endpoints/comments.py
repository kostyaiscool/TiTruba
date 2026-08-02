from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.comments import CommentCRUD
from db.session import db_helper
from modules.auth.models.user import User
from modules.auth.routers.fastapi_users_endpoints import current_active_user
from schemas.commentaries import CommentCreate

router = APIRouter()

@router.get("/comments/{vidid}")
async def get_vidos_comments(
    vidid: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    comments = await CommentCRUD.get_comments_from_video(session, vidid)
    return comments

@router.post("/comments/post")
async def save_comment(
    text: str,
    vidid: int,
    reply_to_id: Optional[int] = None,
    author: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    comment = await CommentCRUD.create(session, CommentCreate(
        text=text,
        video_id=vidid,
        reply_to_id=reply_to_id,
        author=author
    ))
    return comment

@router.get("/replies/{com_id}")
async def get_replies(
        com_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    replies = await CommentCRUD.get_comment(session, com_id)
    return replies