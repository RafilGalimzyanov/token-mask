from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database.core import Base


class ModelORM(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    data_created = Column(DateTime, default=datetime.utcnow)

    user_tokens = relationship("UserTokenORM", secondary="user_token_model")
