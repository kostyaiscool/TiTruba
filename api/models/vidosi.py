from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from api.db.session import Base


class Vidos(Base):
    name: Mapped[str] = mapped_column(String)
    public_name: Mapped[str] = mapped_column(String, default="Хаммам")
    desc: Mapped[str] = mapped_column(String, nullable=True)
    author: Mapped[str] = mapped_column(String(50))
    file_path: Mapped[str] = mapped_column(String(500))
    file_size: Mapped[int] = mapped_column(Integer)
    content_type: Mapped[str] = mapped_column(String(100))
