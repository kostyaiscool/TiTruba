from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.permission import Permission
    from modules.auth.models.user import User
    from models import UserRole
from modules.core.base import Base


class Role(Base):
    name: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False
    )

    user_roles: Mapped[List["UserRole"]] = relationship(
        back_populates="roles",
        cascade="all, delete-orphan",
    )

    permissions: Mapped[List["Permission"]] = relationship(
        back_populates="roles",
    )

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name})>"