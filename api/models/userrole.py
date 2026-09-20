from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.roles import Role
    from modules.auth.models.user import User
from modules.core.base import Base


class UserRole(Base):
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    role: Mapped["Role"] = relationship(
        back_populates="user_roles"
    )

    user: Mapped["User"] = relationship(
        back_populates="user_roles"
    )