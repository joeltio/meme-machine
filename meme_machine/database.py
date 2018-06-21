from settings import DATABASE_URL
import sqlalchemy as sa


def create_engine():
    return sa.create_engine(DATABASE_URL)
