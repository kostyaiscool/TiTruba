from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.session import Base
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
        foreign_keys=[viewer_id]
    )

    video: Mapped["Vidos"] = relationship(
        foreign_keys=[video_id]
    )