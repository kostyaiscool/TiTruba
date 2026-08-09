from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column

from modules.core.base import Base


class UserAuthorInterest(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("vidoss.author_id", ondelete="CASCADE")
    )
    weight: Mapped[float] = mapped_column(
        Float,
        default=0
    )