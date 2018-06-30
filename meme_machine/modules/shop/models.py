from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, String
from sqlalchemy.ext.declarative import declarative_base

from modules.base.models import User

Base = declarative_base()


class ShopItemCategory(Base):
    __tablename__ = "shop_item_category"
    id = Column(Integer, primary_key=True)
    display_name = Column(String, nullable=False)
    code_name = Column(String, nullable=False, unique=True)


class ShopItem(Base):
    __tablename__ = "shop_item"
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey(ShopItemCategory.id),
                         nullable=False)
    name = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    # Constraints
    __tableargs__ = (CheckConstraint("cost > 0"),
                     CheckConstraint("stock >= 0"))


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    initiator_user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    item_id = Column(Integer, ForeignKey(ShopItem.id), nullable=False)
    status = Column(Integer, nullable=False)
