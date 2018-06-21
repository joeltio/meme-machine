from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    snowflake = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    discriminator = Column(String, nullable=False)
    steam_profile_url = Column(String)
    # Constraints
    __tableargs__ = (UniqueConstraint("username", "discriminator"),)
