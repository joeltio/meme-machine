from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from modules.base.models import User

import modules.user_info.settings as user_info_settings

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = "user_info"
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)


def get_steam_profile(session, user_id):
    """Retrieves the steam profile url of the user with the user id.

    :param session: The sqlalchemy session to use to get the steam profile url
    :type session: sqlalchemy session.
    :param user_id: The id of the user to get the steam profile url
    :type user_id: int.
    :returns: str|None -- The steam profile url or None if not found.
    """
    query = session.query(UserInfo).filter_by(
        user_id=user_id,
        name=user_info_settings.USER_INFO_DB_NAME_STEAM_URL).first()

    return query and query.value


def create_steam_profile(session, user_id, url):
    """Creates a new steam profile url record for the user.

    :param session: The sqlalchemy session to use to get the steam profile url
    :type session: sqlalchemy session.
    :param user_id: The id of the user to create the steam profile url
    :type user_id: int.
    :param url: The steam profile url
    :type url: str.
    :returns: None
    """
    user_info = UserInfo(
        user_id=user_id,
        name=user_info_settings.USER_INFO_DB_NAME_STEAM_URL,
        value=url
    )

    session.add(user_info)


def set_steam_profile(session, user_id, url):
    """Sets the steam profile url for the user. If the user did not have a
    steam profile url before, this function will create one.

    :param session: The sqlalchemy session to use to get the steam profile url
    :type session: sqlalchemy session.
    :param user_id: The id of the user to set the steam profile url
    :type user_id: int.
    :param url: The steam profile url
    :type url: str.
    :returns: None
    """
    user_info = session.query(UserInfo).filter_by(
        user_id=user_id,
        name=user_info_settings.USER_INFO_DB_NAME_STEAM_URL).first()

    if user_info is None:
        create_steam_profile(session, user_id, url)
    else:
        user_info.value = url
