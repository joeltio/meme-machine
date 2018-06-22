from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from modules.base.models import User

from modules.credits.settings import STARTING_CREDITS

Base = declarative_base()


class Credit(Base):
    __tablename__ = "credit"
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    credits = Column(Integer, nullable=False)
    # Constraints
    __tableargs__ = (CheckConstraint("credits >= 0"),)


class CreditAction(Base):
    __tablename__ = "credit_action"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    next_active = Column(TIMESTAMP, nullable=False)
    next_daily = Column(TIMESTAMP, nullable=False)


def create_credit(session, user_id, commit=False):
    """Creates a new credit record for the user id. It is assumed that the user
    with the `user_id` already exists.

    :param session: The sqlalchemy session to use to create the user
    :type session: sqlalchemy session.
    :param user_id: The id of the user to create a credit record for.
    :type user_id: int.
    :param commit: Whether to commit after creating the user.
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

    :param session: The sqlalchemy session to use to create the user
    :type session: sqlalchemy session.
    :param user_id: The id of the user to create a credit record for.
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

    :param session: The sqlalchemy session to use to create the user
    :type session: sqlalchemy session.
    :param user_id: The id of the user to create a credit record for.
    :type user_id: int.
    :returns: object -- The database Credit model
    """
    query = get_credit(session, user_id)
    if query:
        return query
    else:
        return create_credit(session, user_id, True)