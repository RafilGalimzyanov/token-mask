from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database.core import Base


class UserTokenORM(Base):
    __tablename__ = "user_token"

    id = Column(Integer, primary_key=True)
    value = Column(String(60))
    name = Column(String)
    description = Column(Text)
    openai_token = Column(String(60))
    request_limit = Column(Integer)
    request_usage = Column(Integer, default=0)
    tiktoken_limit = Column(Integer)
    tokens_usage = Column(Integer, default=0)
    data_created = Column(DateTime, default=datetime.utcnow)

    models = relationship("ModelORM", secondary="user_token_model")
