from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Mapped, relationship

from api.db.session import Base
from models.vidosi import Vidos


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    vidosi: Mapped[List['Vidos']] = relationship(back_populates='categories')
    extension = Column(String)
