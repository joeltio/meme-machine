from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from modules.base.models import User

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = "user_info"
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    name = Column("name", String, nullable=False),
    value = Column("value", String, nullable=False),
