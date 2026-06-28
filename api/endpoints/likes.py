from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.likescrud import LikesCRUD
from db.session import db_helper
from modules.auth.routers.fastapi_users_endpoints import current_active_user
from modules.auth.schemas.user import UserRead

router = APIRouter()

@router.post("/like/{video_id}")
async def like_video(
    video_id: int,
    db: AsyncSession = Depends(
        db_helper.session_getter
    ),
    user: UserRead = Depends(
        current_active_user
    ),
):
    return await LikesCRUD.rate_video(
        db,
        user.id,
        video_id,
        True,
    )


@router.post("/dislike/{video_id}")
async def dislike_video(
    video_id: int,
    db: AsyncSession = Depends(
        db_helper.session_getter
    ),
    user: UserRead = Depends(
        current_active_user
    ),
):
    return await LikesCRUD.rate_video(
        db,
        user.id,
        video_id,
        False,
    )


@router.get("/rating/{video_id}")
async def get_rating(
    video_id: int,
    db: AsyncSession = Depends(
        db_helper.session_getter
    ),
):
    return await LikesCRUD.get_rating(
        db,
        video_id,
    )