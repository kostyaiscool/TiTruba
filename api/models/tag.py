from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.videotag import VideoTag
from modules.core.base import Base


class Tag(Base):
    name: Mapped[str] = mapped_column(
        String(30),
        unique=True
    )

    videos: Mapped[List["VideoTag"]] = relationship(
        back_populates="tag",
        cascade="all, delete-orphan"
    )