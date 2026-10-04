# class Vidos(BaseModel):
#     id: int
#     text: str
#     video_id: int
#     length: int
#     date: PastDatetime
#     author: User
#     author_id: int
#     reply: bool
#     reply_to_id: Optional[int]
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from models import Likes
    from modules.auth.models.user import User
    from models.vidosi import Vidos
from modules.core.base import Base


class Comments(Base):
    text: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String(50))
    # likes: Mapped[List["Likes"]] = relationship(
    #     back_populates="comment",
    #     cascade="all, delete-orphan",
    # )
    creation_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        back_populates="comments"
    )
    video_id: Mapped[int] = mapped_column(
        ForeignKey("vidoss.id")
    )

    video: Mapped["Vidos"] = relationship(
        back_populates="comments"
    )
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("commentss.id"),
        nullable=True
    )

    parent: Mapped[Optional["Comments"]] = relationship(
        "Comments",
        remote_side="Comments.id",
        back_populates="children"
    )

    children: Mapped[List["Comments"]] = relationship(
        "Comments",
        back_populates="parent"
    )