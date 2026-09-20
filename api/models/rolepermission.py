from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.permission import Permission
    from models.roles import Role
from modules.core.base import Base


class RolePermission(Base):
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE")
    )

    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE")
    )

    role: Mapped["Role"] = relationship(
        back_populates="role_permissions"
    )

    permission: Mapped["Permission"] = relationship(
        back_populates="role_permissions"
    )