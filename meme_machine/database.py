from settings import DATABASE_URL
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm


def create_engine():
    return sa.create_engine(DATABASE_URL)


def create_session(*args, **kwargs):
    engine = create_engine()
    Session = sa_orm.sessionmaker(bind=engine)
    return Session(*args, **kwargs)
