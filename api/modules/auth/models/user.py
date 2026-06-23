from typing import TYPE_CHECKING, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.likes import Likes
from models.vidosi import Vidos
from modules.core.base import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    username: Mapped[str] = mapped_column(String(20), unique=True)
    # likes: Mapped["Likes"] = relationship(back_populates="users")
    videos: Mapped[List["Vidos"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )

    likes: Mapped[List["Likes"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)