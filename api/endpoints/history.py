from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud.history import HistoryCRUD
from db.session import db_helper
from modules.auth.routers.fastapi_users_endpoints import current_active_user
from modules.auth.schemas.user import UserRead

router = APIRouter()

# @router.get("/history/{user_id}")
# async def get_user_history(
#         user_id: int,
#         session: AsyncSession = Depends(db_helper.session_getter),
# ):
#     history = await HistoryCRUD.get_history_by_viewer(session, user_id)
#     return history

@router.post("/history/add/{viewer_id}")
async def add_video_user_history(
        viewer_id: int,
        video_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    history = await HistoryCRUD.add_video_history(session, viewer_id, video_id)
    if history is None:
        raise HTTPException(
            status_code=404,
            detail="Видео не найдено"
        )
    return history

@router.get("/history/")
async def get_user_history(
        user: UserRead = Depends(current_active_user),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    history = await HistoryCRUD.get_history_logged(session, user)
    return history