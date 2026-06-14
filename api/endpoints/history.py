from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.history import HistoryCRUD
from db.session import db_helper

router = APIRouter()

@router.get("/history/{user_id}")
async def get_user_history(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    history = await HistoryCRUD.get_history_by_viewer(session, user_id)
    return history

@router.post("/history/add/{viewer_id}")
async def add_video_user_history(
        viewer_id: int,
        video_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    history = await HistoryCRUD.add_video_history(session, viewer_id, video_id)
    return history

