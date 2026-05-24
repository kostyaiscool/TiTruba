from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from modules.auth.models.user import User
from db.session import db_helper

async def get_users_db(session: AsyncSession = Depends(db_helper.session_getter)):
    yield User.get_db(session=session)

