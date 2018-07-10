from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

from modules.base.models import User

import modules.raffle.settings as raffle_settings

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
    status = Column(String, nullable=False)
    # Constraints
    __tableargs__ = (CheckConstraint("max_slots > 0"),)


def get_current_raffle(session):
    """Retrieves the first raffle found that has the status of OPEN.

    :param session: The sqlalchemy session to use to get the current raffle
    :type session: sqlalchemy session.
    :returns: object|None -- The database Raffle model if any found, None if
    there are no open raffles.
    """
    query = session.query(Raffle).filter_by(
        status=raffle_settings.RAFFLE_DB_STATUS_OPEN).first()

    return query


def create_raffle(session, item_name, max_slots, commit=False):
    """Creates a new raffle record with the item name and max slots. The new
    raffle record will have the status of OPEN.

    Does not check if there is already an ongoing raffle.

    :param session: The sqlalchemy session to use to get the current raffle
    :type session: sqlalchemy session.
    :param item_name: The name of the item being raffled
    :type item_name: str.
    :param max_slots: The maximum number of slots the raffle can hold
    :type max_slots: int.
    :param commit: Whether to commit after creating the raffle record.
    :type commit: bool.
    :returns: object -- The database Raffle model created/to be created
    (Depending on whether it was committed).
    """
    raffle = Raffle(item=item_name, max_slots=max_slots,
                    status=raffle_settings.RAFFLE_DB_STATUS_OPEN)

    session.add(raffle)

    if commit:
        session.commit()

    return raffle
