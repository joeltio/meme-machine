from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Credit(Base):
    __tablename__ = "credit"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    credits = Column(Integer, nullable=False)
    # Constraints
    __tableargs__ = (CheckConstraint("credits >= 0"),)


class CreditAction(Base):
    __tablename__ = "credit_action"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    next_active = Column(TIMESTAMP, nullable=False)
    next_daily = Column(TIMESTAMP, nullable=False)
