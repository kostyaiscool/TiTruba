from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.tags import TagCRUD
from db.session import db_helper

router = APIRouter()

@router.get("/tags/{tag_id}")
async def get_tag(
        tag_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    tag = await TagCRUD.get_tag(session, tag_id)
    return tag

@router.post("/tags/add")
async def add_tag(
        tag_name: str,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    tag = await TagCRUD.add_tag(session, tag_name)
    return tag

@router.delete("/tags/delete")
async def remove_tag(
        tag_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    await TagCRUD.remove_tag(session, tag_id)
    return True