from sqlalchemy import Column, Integer, String

from database.core import Base


class AdminORM(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    token = Column(String(30))
