from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.tag import Tag
from models.vidosi import Vidos
from modules.core.base import Base


class VideoTag(Base):

    video_id: Mapped[int] = mapped_column(
        ForeignKey("vidoss.id", ondelete="CASCADE")
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE")
    )

    video: Mapped["Vidos"] = relationship(
        back_populates="tags"
    )

    tag: Mapped["Tag"] = relationship(
        back_populates="videos"
    )