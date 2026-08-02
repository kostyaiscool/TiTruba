from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.tag import Tag
from modules.auth.models.user import User
from modules.core.base import Base


class UserTagInterest(Base):

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE")
    )

    weight: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    user: Mapped["User"] = relationship()

    tag: Mapped["Tag"] = relationship()