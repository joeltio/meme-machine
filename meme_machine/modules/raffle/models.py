from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

from modules.base.models import User

Base = declarative_base()


class RaffleSlot(Base):
    __tablename__ = "raffle_slot"
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    slots = Column(Integer, nullable=False)
    # Constraints
    __tableargs__ = (CheckConstraint("slots > 0"),)


class Raffle(Base):
    __tablename__ = "raffle"
    id = Column(Integer, primary_key=True)
    max_slots = Column(Integer, nullable=False)
    item = Column(String, nullable=False)
    # Constraints
    __tableargs__ = (CheckConstraint("max_slots > 0"),)
