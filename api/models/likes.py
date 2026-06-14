from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.session import Base
from models.vidosi import Vidos
from modules.auth.models.user import User


class Likes(Base):
    liker_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    video_id: Mapped[int] = mapped_column(
        ForeignKey("vidoss.id")
    )
    liker: Mapped["User"] = relationship(
        foreign_keys=[liker_id]
    )
    video: Mapped["Vidos"] = relationship(
        foreign_keys=[video_id]
    )
    rating: Mapped[bool] = mapped_column(
        Boolean, default=None, nullable=True
    )