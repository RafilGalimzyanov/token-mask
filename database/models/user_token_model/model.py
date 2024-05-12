from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database.core import Base


class UserTokenModelORM(Base):
    __tablename__ = "user_token_model"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_token_id = Column(Integer, ForeignKey("user_token.id"), primary_key=True)
    model_id = Column(Integer, ForeignKey("model.id"), primary_key=True)

    user_token = relationship("UserTokenORM", backref="model_associations")
    model = relationship("ModelORM", backref="user_token_associations")
