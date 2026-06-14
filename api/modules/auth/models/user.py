from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.likes import Likes
from models.vidosi import Vidos
from modules.core.base import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    username: Mapped[str] = mapped_column(String(20), unique=True)
    like_id: Mapped[int] = mapped_column(ForeignKey("likess.id"))
    likes: Mapped["Likes"] = relationship(back_populates="users")
    # dislikes: Mapped["Vidos"] = relationship(back_populates="users")
    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)