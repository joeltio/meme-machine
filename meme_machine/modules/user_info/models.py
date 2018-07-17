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
