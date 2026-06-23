from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.session import Base
from modules.auth.models.user import User


class Subscriber(Base):

    subscriber_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    subscribed_to_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    # кто подписался
    subscriber: Mapped["User"] = relationship(
        foreign_keys=[subscriber_id]
    )

    # на кого подписались
    subscribed_to: Mapped["User"] = relationship(
        foreign_keys=[subscribed_to_id]
    )