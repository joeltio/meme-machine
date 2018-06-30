from modules.shop.actions import (shop, shops, admin_shop, admin_set_stock,
                                  admin_update_category)

COMMANDS = {
    "shop": shop,
    "shops": shops,
    "admin-shop": admin_shop,
    "admin-set-stock": admin_set_stock,
    "admin-update-category": admin_update_category,
}
