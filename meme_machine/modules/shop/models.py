from sqlalchemy import (Column, Integer, String, ForeignKey, CheckConstraint,
                        UniqueConstraint)
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
                     CheckConstraint("stock >= 0"),
                     UniqueConstraint("category_id", "code_name",
                                      name="uq_category_id_code_name"))


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    initiator_user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    item_id = Column(Integer, ForeignKey(ShopItem.id), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    # Constraints
    __tableargs__ = (CheckConstraint("amount > 0"),)


def to_code_name(item_name):
    """Converts an item name to a code name

    :param item_name: The name of the item
    :type item_name: str.
    :returns: str -- The code name of the item
    """
    return item_name.lower().replace(" ", "_")


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


def get_transactions(session, initiator_id=None, item_id=None, status=None):
    """Retrieves all the transactions filtered by the initiator's id,
    item's id and/or status.

    :param session: The sqlalchemy session to use to get the transactions
    :type session: sqlalchemy session.
    :param initiator_id: Filter the transaction's initiator's user id
    :type initiator_id: int.
    :param item_id: Filter the transaction's item's id
    :type item_id: int.
    :param status: Filter the status of the transaction
    :type status: str.
    :returns: list[objects] -- A list of the database Transaction models.
    """
    filters = {}
    if initiator_id is not None:
        filters["initiator_id"] = initiator_id
    if item_id is not None:
        filters["item_id"] = item_id
    if status is not None:
        filters["status"] = status

    return session.query(Transaction).filter_by(**filters).all()


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
                  item_code=None, item_name=None):
    """Retrieves the database ShopItem model using one of the following:
    ```
    (id)
    (category_code, item_code)
    (category_id, item_code)
    ```
    `item_name` will be converted to `item_code`.

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
    :param item_name: The shop item's name that will be converted to
    `item_code` before searching.
    :type item_name: str.
    :returns: object|None -- The database ShopItem model if found, None if
    there is no such record.
    """
    if item_name is not None and item_code is None:
        # Convert to item code if only the item name is given
        item_code = to_code_name(item_name)

    if id is not None:
        # Only id
        filters = {"id": id}
    elif (category_code and item_code) is not None:
        # Category and item code
        category = get_shop_category(session, category_code=category_code)

        if category is None:
            return None

        filters = {"code_name": item_code, "category_id": category.id}
    elif (category_id and item_code) is not None:
        # Category id and item code
        filters = {"code_name": item_code, "category_id": category_id}
    else:
        return None

    query = session.query(ShopItem).filter_by(**filters).all()

    if query:
        return query[0]
    else:
        return None


def get_transaction(session, id):
    """Retrieves the database Transaction model using the transaction id.

    :param session: The sqlalchemy session to use to get the transaction
    :type session: sqlalchemy session.
    :param id: The transaction's id
    :type id: int.
    :returns: object|None -- The database Transaction model if found, None if
    there is no such record.
    """
    query = session.query(Transaction).filter_by(id=id).all()

    if query:
        return query[0]
    else:
        return None


def create_shop_item(session, category_id, name, cost, stock, commit=False):
    """Creates a new shop item record within the category. It is assumed that
    the `category_id` already exists.
    The code name of the shop item will be set using `to_code_name`.

    :param session: The sqlalchemy session to use to create the shop item
    :type session: sqlalchemy session.
    :param category_id: The id of the category the item belongs to.
    :type category_id: int.
    :param name: The item's name
    :type name: str.
    :param cost: The item's cost
    :type cost: int.
    :param stock: How many items there are in the shop
    :type stock: int.
    :param commit: Whether to commit after creating the shop item record.
    :type commit: bool.
    :returns: object -- The database ShopItem model created/to be created
    (Depending on whether it was committed).
    """
    shop_item = ShopItem(
        category_id=category_id,
        name=name,
        code_name=to_code_name(name),
        cost=cost,
        stock=stock
    )

    session.add(shop_item)

    if commit:
        session.commit()

    return shop_item


def create_shop_category(session, display_name, code_name,
                         color, thumbnail_url, commit=False):
    """Creates a new shop item category record.

    :param session: The sqlalchemy session to use to create the shop item
    category
    :type session: sqlalchemy session.
    :param display_name: The category's display name
    :type display_name: str.
    :param code_name: Thte category's code name used to refer to the category
    :type code_name: str.
    :param color: The color of the embed when showing the items in the category
    as a 6 digit hex string (e.g. F10D2E).
    :type color: str.
    :param thumbnail_url: The thumbnail's url shown when showing items in the
    category
    :type thumbnail_url: str.
    :param commit: Whether to commit after creating the shop item category
    record.
    :type commit: bool.
    :returns: object -- The database ShopItemCategory model created/to be
    created (Depending on whether it was committed).
    """
    shop_category = ShopItemCategory(
        display_name=display_name,
        code_name=code_name,
        color=color,
        thumbnail_url=thumbnail_url
    )

    session.add(shop_category)

    if commit:
        session.commit()

    return shop_category
