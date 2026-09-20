from typing import TYPE_CHECKING, List, Iterable

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.likes import Likes
    from models.commentaries import Comments
    from models.roles import Role
    from models.userrole import UserRole

from modules.core.base import Base

class User(Base, SQLAlchemyBaseUserTable[int]):
    username: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )

    user_roles: Mapped[List["UserRole"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    likes: Mapped[List["Likes"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    comments: Mapped[List["Comments"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)

    def has_role(self, role_name: str) -> bool:
        return any(
            user_role.role.name == role_name
            for user_role in self.user_roles
        )

    def has_any_role(self, *role_names: str) -> bool:
        return any(
            user_role.role.name in role_names
            for user_role in self.user_roles
        )