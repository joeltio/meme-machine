from datetime import datetime

from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from modules.base.models import User, Config

from modules.credits.settings import (STARTING_CREDITS, DAILY_CONFIG_MIN_NAME,
                                      DAILY_CONFIG_MAX_NAME,
                                      DAILY_CONFIG_MIN_DEFAULT,
                                      DAILY_CONFIG_MAX_DEFAULT)

Base = declarative_base()


class Credit(Base):
    __tablename__ = "credit"
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    credits = Column(Integer, nullable=False)
    # Constraints
    __tableargs__ = (CheckConstraint("credits >= 0"),)


class CreditAction(Base):
    __tablename__ = "credit_action"

    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    next_active = Column(TIMESTAMP, nullable=False)
    next_daily = Column(TIMESTAMP, nullable=False)


def create_credit(session, user_id, commit=False):
    """Creates a new credit record for the user id. It is assumed that the user
    with the `user_id` already exists.
    The user will start with the `STARTING_CREDITS` defined in the credits
    settings.

    :param session: The sqlalchemy session to use to create the credit record
    :type session: sqlalchemy session.
    :param user_id: The id of the user to create a credit record for.
    :type user_id: int.
    :param commit: Whether to commit after creating the credit record.
    :type commit: bool.
    :returns: object -- The database Credit model created/to be created
    (Depending on whether it was committed).

    """
    credit = Credit(
        user_id=user_id,
        credits=STARTING_CREDITS,
    )

    session.add(credit)

    if commit:
        session.commit()

    return credit


def get_credit(session, user_id):
    """Gets the credit record of the user with the `user_id`.

    :param session: The sqlalchemy session to use to get the credit
    :type session: sqlalchemy session.
    :param user_id: The credit record's user's id.
    :type user_id: int.
    :returns: object|None -- The database Credit model if such a record exists.
    None if there is no record.

    """
    query = session.query(Credit).filter_by(user_id=user_id).all()

    if query:
        return query[0]
    else:
        return None


def get_or_create_credit(session, user_id):
    """Gets the credit model if it already exists. If not, creates and commits
    the credit model. This assumes that the user with the `user_id` exists.

    :param session: The sqlalchemy session to use to get or create the credit
    record
    :type session: sqlalchemy session.
    :param user_id: The id of the user to search or create a credit record for.
    :type user_id: int.
    :returns: object -- The database Credit model
    """
    query = get_credit(session, user_id)
    if query:
        return query
    else:
        return create_credit(session, user_id, True)


def create_credit_action(session, user_id, commit=False):
    """Creates a new credit action record for the user id. It is assumed that
    the user with the `user_id` already exists.
    The `next_active` and `next_daily` will be set to the current time.

    :param session: The sqlalchemy session to use to create the credit action
    :type session: sqlalchemy session.
    :param user_id: The id of the user to create a credit action record for.
    :type user_id: int.
    :param commit: Whether to commit after creating the credit action record.
    :type commit: bool.
    :returns: object -- The database Credit Action model created/to be created
    (Depending on whether it was committed).

    """
    credit_action = CreditAction(
        user_id=user_id,
        next_active=datetime.now(),
        next_daily=datetime.now(),
    )

    session.add(credit_action)

    if commit:
        session.commit()

    return credit_action


def get_credit_action(session, user_id):
    """Gets the credit action record of the user with the `user_id`.

    :param session: The sqlalchemy session to use to get the credit action
    :type session: sqlalchemy session.
    :param user_id: The credit action's record's user's id.
    :type user_id: int.
    :returns: object|None -- The database Credit Action model if such a record
    exists. None if there is no record.

    """
    query = session.query(CreditAction).filter_by(user_id=user_id).all()

    if query:
        return query[0]
    else:
        return None


def get_or_create_credit_action(session, user_id):
    """Gets the credit action model if it already exists. If not, creates and
    commits the credit action model. This assumes that the user with the
    `user_id` exists.

    :param session: The sqlalchemy session to use to get or create the credit
    action record
    :type session: sqlalchemy session.
    :param user_id: The id of the user to search or create a credit action
    record for.
    :type user_id: int.
    :returns: object -- The database Credit Action model
    """
    query = get_credit_action(session, user_id)
    if query:
        return query
    else:
        return create_credit_action(session, user_id, True)


def get_or_create_daily_range(session):
    """Gets the range of daily values to give the the user. The range is
    inclusive, i.e. [min, max]. If either the daily minimum or maximum is not
    found, they will be created using the default in the settings.

    :param session: The sqlalchemy session to use to query for the daily range
    in the config table.
    :type session: sqlalchemy session
    :returns: (int, int) -- The (min, max) of daily values that can be awarded
    """
    min_query = session.query(Config).filter_by(
        name=DAILY_CONFIG_MIN_NAME).all()

    if not min_query:
        # Create and default to DAILY_CONFIG_MIN_DEFAULT
        min_config = Config(
            name=DAILY_CONFIG_MIN_NAME,
            value=DAILY_CONFIG_MIN_DEFAULT,
        )

        session.add(min_config)
    else:
        min_config = min_query[0]

    max_query = session.query(Config).filter_by(
        name=DAILY_CONFIG_MAX_NAME).all()

    if not max_query:
        max_config = Config(
            name=DAILY_CONFIG_MAX_NAME,
            value=DAILY_CONFIG_MAX_DEFAULT,
        )

        session.add(max_config)
    else:
        max_config = max_query[0]

    session.commit()

    return (min_config, max_config)
