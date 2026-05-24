from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from modules.auth.dependencies.users import get_users_db
from modules.auth.user_manager import UserManager


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_users_db)):
    yield UserManager(user_db)