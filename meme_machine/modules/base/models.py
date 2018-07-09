from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists

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


class Config(Base):
    __tablename__ = "config"
    name = Column(String, primary_key=True)
    value = Column(String, nullable=False)


def user_exists(session, discord_snowflake):
    """Checks if a user exists in the user table based on the discord
    snowflake

    :param session: The sqlalchemy session to use to create the user
    :type session: sqlalchemy session.
    :param discord_snowflake: The discord snowflake to check against the
    database
    :type discord_snowflake: str.
    :returns: bool -- Whether the user exists.

    """
    return session.query(exists().where(User.id == discord_snowflake)).scalar()


def create_user(session, discord_user, commit=False):
    """Creates a new user

    :param session: The sqlalchemy session to use to create the user
    :type session: sqlalchemy session.
    :param discord_user: The discord.py User object to use to create a user
    record.
    :type discord_user: discord.py User object.
    :param commit: Whether to commit after creating the user.
    :type commit: bool.
    :returns: object -- The database User model created/to be created
    (Depending on whether it was committed).

    """
    new_user = User(
        snowflake=discord_user.id,
        username=discord_user.name,
        discriminator=str(discord_user.discriminator),
    )

    session.add(new_user)

    if commit:
        session.commit()

    return new_user


def get_user(session, discord_snowflake=None, id=None):
    """Gets the user based on the discord snowflake or the user record id.

    :param session: The sqlalchemy session to use to create the user
    :type session: sqlalchemy session.
    :param discord_snowflake: The discord snowflake to identify the user
    :type discord_snowflake: str.
    :param id: The user record id.
    :type: int.
    :returns: object|None -- The database User model if found, None if no user
    was found

    """
    if discord_snowflake is None:
        query = session.query(User).filter_by(id=id).all()
    else:
        query = session.query(User).filter_by(
            snowflake=discord_snowflake).all()

    if query:
        return query[0]
    else:
        return None


def get_or_create_user(session, discord_user):
    """Gets the user if it already exists. If not, creates and commits the
    user.

    :param session: The sqlalchemy session to use to create the user
    :type session: sqlalchemy session.
    :param discord_user: The discord.py User object to use to create a user
    record.
    :type discord_user: discord.py User object.
    :returns: object -- The database User model of the fetched/created user

    """
    query = get_user(session, discord_snowflake=discord_user.id)
    if query:
        return query
    else:
        return create_user(session, discord_user, True)
