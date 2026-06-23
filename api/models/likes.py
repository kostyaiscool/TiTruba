from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.session import Base
if TYPE_CHECKING:
    from modules.auth.models.user import User
    from models.vidosi import Vidos


class Likes(Base):
    # liker_id: Mapped[int] = mapped_column(
    #     ForeignKey("user.id")
    # )
    # video_id: Mapped[int] = mapped_column(
    #     ForeignKey("vidos.id")
    # )
    # liker: Mapped["User"] = relationship(
    #     foreign_keys=[liker_id]
    # )
    # video: Mapped["Vidos"] = relationship(
    #     foreign_keys=[video_id]
    # )
    # rating: Mapped[bool] = mapped_column(
    #     Boolean, default=None, nullable=True
    # )
    liker_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    video_id: Mapped[int] = mapped_column(
        ForeignKey("vidos.id", ondelete="CASCADE")
    )

    rating: Mapped[bool] = mapped_column(Boolean)

    user: Mapped["User"] = relationship(
        back_populates="likes"
    )

    video: Mapped["Vidos"] = relationship(
        back_populates="likes"
    )