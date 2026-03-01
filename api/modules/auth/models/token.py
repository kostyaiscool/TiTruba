from typing import Optional

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AccessToken(DeclarativeBase):
    pass


class RefreshToken(DeclarativeBase):
    pass