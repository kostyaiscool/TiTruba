from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.permission import Permission
    from models.rolepermission import RolePermission
    from models.userrole import UserRole
from modules.core.base import Base


class Role(Base):
    name: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False
    )

    user_roles: Mapped[List["UserRole"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )

    role_permissions: Mapped[List["RolePermission"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )

    # только для чтения, связи меняются через role_permissions
    permissions: Mapped[List["Permission"]] = relationship(
        secondary="role_permissions",
        back_populates="roles",
        viewonly=True,
    )

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name})>"
