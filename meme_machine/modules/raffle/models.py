from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from modules.base.models import User

import modules.raffle.settings as raffle_settings

Base = declarative_base()


class Raffle(Base):
    __tablename__ = "raffle"
    id = Column(Integer, primary_key=True)
    max_slots = Column(Integer, nullable=False)
    item = Column(String, nullable=False)
    status = Column(String, nullable=False)
    # Constraints
    __tableargs__ = (CheckConstraint("max_slots > 0"),)


class RaffleSlot(Base):
    __tablename__ = "raffle_slot"
    id = Column(Integer, primary_key=True)
    raffle_id = Column(Integer, ForeignKey(Raffle.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    slots = Column(Integer, nullable=False)
    # Constraints
    __tableargs__ = (CheckConstraint("slots > 0"),)


def get_raffle(session, raffle_id=None):
    """Retrieves the raffle with the raffle id. Retrieves the first raffle
    found that has the status of OPEN if raffle id is None.

    :param session: The sqlalchemy session to use to get the current raffle
    :type session: sqlalchemy session.
    :param raffle_id: The id of the raffle to retrieve
    :type raffle_id: int.
    :returns: object|None -- The database Raffle model if any found, None if
    there are no open raffles.
    """
    if raffle_id is None:
        query = session.query(Raffle).filter_by(
            status=raffle_settings.RAFFLE_DB_STATUS_OPEN).first()
    else:
        query = session.query(Raffle).filter_by(id=raffle_id).first()

    return query


def get_raffle_slot(session, user_id, raffle_id=None):
    """Retrieves the raffle slot filtered by user id and raffle id.
    If raffle id is None, the current raffle will be used

    :param session: The sqlalchemy session to use to get the raffle slot
    :type session: sqlalchemy session.
    :param user_id: The id of the user to whom the raffle slot belongs to
    :type user_id: int.
    :param raffle_id: The raffle id
    :type raffle_id: int.
    :returns: object|None The database RaffleSlot model if any found, None if
    there are no RaffleSlots matching the filters or if there are no open
    raffles (for when raffle_id is None).
    """
    if raffle_id is None:
        current_raffle = get_raffle(session)

        if current_raffle is None:
            return

        raffle_id = current_raffle.id

    return session.query(RaffleSlot).filter_by(
        raffle_id=raffle_id, user_id=user_id).first()


def get_raffle_slots(session, raffle_id):
    """Retrieves the raffle slots for the raffle id

    :param session: The sqlalchemy session to use to get the raffle slots
    :type session: sqlalchemy session.
    :param raffle_id: The raffle id to filter the raffle slots by.
    :type raffle_id: int.
    :returns: list[object] -- A list of the database RaffleSlot model if
    any found, an empty list if there are no open raffles or there are no
    raffle slots.
    """
    return session.query(RaffleSlot).filter_by(raffle_id=raffle_id).all()


def get_user_total_raffle_slots_slots(session, user_id, raffle_id=None):
    """Aggregates the user's raffle slots slots.
    In other words, returns the total slots that the user has bought for a
    raffle.
    If raffle id is None, the current raffle will be used

    :param session: The sqlalchemy session to use to get the raffle slots
    :type session: sqlalchemy session.
    :param raffle_id: The raffle id the user is in.
    :type raffle_id: int.
    :param user_id: The id of the user to whom the raffle slots belongs to
    :type user_id: int.
    :returns: int|None -- The number of slots the user has for the given
    raffle. None if no raffle id was given and there are no current raffles.
    """
    if raffle_id is None:
        current_raffle = get_raffle(session)

        if current_raffle is None:
            return

        raffle_id = current_raffle.id

    query = session.query(func.sum(RaffleSlot.slots)).filter_by(
        raffle_id=raffle_id, user_id=user_id).first()

    if query[0] is None:
        return 0
    else:
        return query[0]


def get_total_raffle_slots_slots(session, raffle_id=None):
    """Retrieves the sum of all `slots` in every RaffleSlot record that has the
    raffle id.
    If raffle_id is None, it will default to the current raffle.

    :param session: The sqlalchemy session to use to get the raffle slots
    :type session: sqlalchemy session.
    :param raffle_id: The raffle id to filter the raffle slots by.
    :type raffle_id: int.
    :returns: int -- The total number of raffle slots slots.
    """
    if raffle_id is None:
        current_raffle = get_raffle(session)
        raffle_id = current_raffle.id

    query = session.query(func.sum(RaffleSlot.slots)) \
        .filter_by(raffle_id=raffle_id).first()

    if query[0] is None:
        return 0
    else:
        return query[0]


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


def create_raffle_slot(session, user_id, slots, raffle_id=None, commit=False):
    """Creates a raffle slot record for the raffle id. If no raffle id is given
    the current raffle will be used.

    :param session: The sqlalchemy session to use to create the raffle slot
    :type session: sqlalchemy session.
    :param user_id: The id of the user who should own the slots
    :type user_id: int.
    :param slots: The number of slots
    :type slots: int.
    :param raffle_id: The raffle id to create slots for
    :type raffle_id: int.
    :param commit: Whether to commit after creating the raffle slot record.
    :type commit: bool.
    :returns: object -- The database RaffleSlot model created/to be created
    (Depending on whether it was committed).
    """
    # If raffle_id is None, it will get the current raffle
    raffle = get_raffle(session, raffle_id)

    # Create the raffle slot
    raffle_slot = RaffleSlot(raffle_id=raffle.id, user_id=user_id,
                             slots=slots)
    session.add(raffle_slot)

    if commit:
        session.commit()

    return raffle_slot
