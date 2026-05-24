from datetime import datetime
from typing import List, TYPE_CHECKING, Optional
from sqlalchemy import BigInteger, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class User(DeclarativeBase):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[Optional[str]] = mapped_column(String(32))
    # first_name: Mapped[str] = mapped_column(String(64))
    # last_name: Mapped[Optional[str]] = mapped_column(String(64))
    language_code: Mapped[Optional[str]] = mapped_column(String(10))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)