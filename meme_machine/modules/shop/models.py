from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, String
from sqlalchemy.ext.declarative import declarative_base

from modules.base.models import User

Base = declarative_base()


class ShopItemCategory(Base):
    __tablename__ = "shop_item_category"
    id = Column(Integer, primary_key=True)
    display_name = Column(String, nullable=False)
    code_name = Column(String, nullable=False, unique=True)
    color = Column(String, nullable=False)
    thumbnail_url = Column(String(6), nullable=False)


class ShopItem(Base):
    __tablename__ = "shop_item"
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey(ShopItemCategory.id),
                         nullable=False)
    name = Column(String, nullable=False)
    code_name = Column(String, nullable=False)
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


def get_shop_items(session, category_code=None, category_id=None):
    """Retrieves shop items that can be filtered by category.

    :param session: The sqlalchemy session to use to get the shop items
    :type session: sqlalchemy session.
    :param category_code: The code of the category to filter by
    :type category_code: str.
    :param category_id: The id of the category to filter by
    :type category_id: int.
    :returns: list[object] -- A list of the database ShopItem models.
    """
    if category_code is not None:
        category = get_shop_category(session, category_code=category_code)

        if category is None:
            return []

        filters = {"category_id": category.id}
    elif category_id is not None:
        filters = {"category_id": category_id}
    else:
        return session.query(ShopItem).all()

    return session.query(ShopItem).filter_by(**filters).all()


def get_categories(session):
    """Retrieves all the categories

    :param session: The sqlalchemy session to use to get the categories
    :type session: sqlalchemy session.
    :returns: list[object] -- A list of the database ShopItemCategory models.
    """
    return session.query(ShopItemCategory).all()


def get_shop_category(session, id=None, category_code=None):
    """Retrieves the database ShopItemCategory model associated with the id or
    category code

    :param session: The sqlalchemy session to use to get the shop category
    :type session: sqlalchemy session.
    :param id: The id of the shop category
    :type id: int.
    :param category_code: The category code
    :type category_code: str.
    :returns: object|None -- The database ShopItemCategory model if found, None
    if there is no such record.
    """
    if (id or category_code) is None:
        return None

    filters = {
        "id": id,
        "code_name": category_code,
    }

    # Remove None values
    filters = dict(filter(lambda x: x[1] is not None, filters.items()))

    query = session.query(ShopItemCategory).filter_by(**filters).all()

    if query:
        return query[0]
    else:
        return None


def get_shop_item(session, id=None, category_code=None, category_id=None,
                  item_code=None):
    """Retrieves the database ShopItem model using one of the following:
    ```
    (id)
    (category_code, item_code)
    (category_id, item_code)
    ```

    :param session: The sqlalchemy session to use to get the shop item
    :type session: sqlalchemy session.
    :param id: The id of the shop item
    :type id: int.
    :param category_code: The category code that the shop item belongs to
    :type category_code: str.
    :param category_id: The id of the category the shop item belongs to
    :type category_id: int.
    :param item_code: The shop item's code
    :type item_code: str.
    :returns: object|None -- The database ShopItem model if found, None if
    there is no such record.
    """
    if id is not None:
        # Only id
        filters = {"id": id}
    elif (category_code or item_code) is not None:
        # Category and item code
        category = get_shop_category(session, category_code=category_code)

        if category is None:
            return None

        filters = {"code_name": item_code, "category_id": category.id}
    elif (category_id or item_code) is not None:
        # Category id and item code
        filters = {"code_name": item_code, "category_id": category.id}
    else:
        return None

    query = session.query(ShopItem).filter_by(**filters).all()

    if query:
        return query[0]
    else:
        return None
