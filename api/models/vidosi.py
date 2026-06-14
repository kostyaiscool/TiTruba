from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

from api.db.session import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.likes import Likes


class Vidos(Base):
    name: Mapped[str] = mapped_column(String)
    public_name: Mapped[str] = mapped_column(String, default="Хаммам")
    desc: Mapped[str] = mapped_column(String, nullable=True)
    author: Mapped[str] = mapped_column(String(50))
    file_path: Mapped[str] = mapped_column(String(500))
    file_size: Mapped[int] = mapped_column(Integer)
    content_type: Mapped[str] = mapped_column(String(100))
    views: Mapped[int] = mapped_column(Integer, default=0)
    likes_c: Mapped[int] = mapped_column(Integer, default=0)
    dislikes_c: Mapped[int] = mapped_column(Integer, default=0)
    like_id: Mapped[int] = mapped_column(ForeignKey("likess.id"))
    likes: Mapped["Likes"] = relationship(back_populates="users")
