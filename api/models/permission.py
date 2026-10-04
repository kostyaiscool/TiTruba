from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.roles import Role
    from models.rolepermission import RolePermission

from modules.core.base import Base


class Permission(Base):
    name: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False
    )

    role_permissions: Mapped[List["RolePermission"]] = relationship(
        back_populates="permission",
        cascade="all, delete-orphan",
    )

    # только для чтения, связи меняются через role_permissions
    roles: Mapped[List["Role"]] = relationship(
        secondary="role_permissions",
        back_populates="permissions",
        viewonly=True,
    )

    def __repr__(self) -> str:
        return f"<Permission(id={self.id}, name={self.name})>"
