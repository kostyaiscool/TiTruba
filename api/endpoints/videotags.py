from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.videotagcrud import VideoTagCRUD
from db.session import db_helper
from models import Tag
from models.vidosi import Vidos

router = APIRouter()
@router.get("/videotags/all")
async def get_all_tags(
        session: AsyncSession = Depends(db_helper.session_getter)
):
    result = await VideoTagCRUD.get_tags(session)
    return result
@router.get("/videotags/{tag_id}")
async def get_tag(
        tag_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    tag = await VideoTagCRUD.get_tag(session, tag_id)
    return tag

@router.get("/videotags/videos/{tag_id}")
async def get_tag_videos(
        tag_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    videos = await VideoTagCRUD.get_tag_videos(session, tag_id)
    return videos

@router.post("/videotags/add")
async def add_tag(
        video: int,
        tag: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    tag = await VideoTagCRUD.add_tag(session, tag, video)
    return tag

@router.delete("/videotags/delete")
async def remove_tag(
        tag_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    await VideoTagCRUD.remove_tag(session, tag_id)
    return True

@router.get("/videotags/tags/{vid_id}")
async def get_tag_videos(
        vid_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    tags = await VideoTagCRUD.get_tags_by_videos(session, vid_id)
    return tags

