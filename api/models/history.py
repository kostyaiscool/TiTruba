from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.session import Base
if TYPE_CHECKING:
    from models.vidosi import Vidos
from modules.auth.models.user import User


class History(Base):
    viewer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    video_id: Mapped[int] = mapped_column(
        ForeignKey("vidoss.id")
    )

    viewer: Mapped["User"] = relationship(
        foreign_keys=[viewer_id],
    )

    video: Mapped["Vidos"] = relationship(
        foreign_keys=[video_id],
    )
    watch_percent: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    liked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True
    )

    watched_at: Mapped[datetime]