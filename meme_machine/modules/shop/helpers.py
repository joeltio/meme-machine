import modules.shop.models as shop_models


def get_and_organize_items(session):
    """Retrieves and organizes the shop items into their categories

    :param session: The sqlalchemy session to use to get the shop items and
    categories
    :type session: sqlalchemy session.
    :returns: dict -- Returns a dictionary. The keys are the category's id. The
    values contain a list of the database ShopItems models. e.g.
    ```
    {
        1: [
            <ShopItem A>,
            <ShopItem B>,
            <ShopItem C>
        ],
        2: [
            <ShopItem D>,
            <ShopItem E>,
            <ShopItem F>
        ]
    }
    ```
    """
    items = shop_models.get_shop_items(session)
    organized_items = {}

    for item in items:
        cat_id = item.category_id
        organized_items[cat_id] = organized_items.get(cat_id, []) + [item]

    return organized_items
