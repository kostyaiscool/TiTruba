from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

from api.db.session import Base


class Vidos(Base):
    __tablename__ = "vidos"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    creation_date = Column(DateTime)
    desc = Column(String)
    author = Column(String)
