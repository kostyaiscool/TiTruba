from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.roles import Role
    from models import RolePermission

from modules.core.base import Base


class Permission(Base):
    name: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False
    )

    role_permissions: Mapped[List["RolePermission"]] = relationship(
        back_populates="permissions",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Permission(id={self.id}, name={self.name})>"