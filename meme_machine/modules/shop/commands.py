from modules.shop.actions import (shop, shops, admin_shop, admin_set_stock,
                                  admin_update_category, admin_add_item,
                                  admin_remove_item, admin_add_category,
                                  admin_remove_category)

COMMANDS = {
    "shop": shop,
    "shops": shops,
    "admin-shop": admin_shop,
    "admin-set-stock": admin_set_stock,
    "admin-update-category": admin_update_category,
    "admin-add-item": admin_add_item,
    "admin-remove-item": admin_remove_item,
    "admin-add-category": admin_add_category,
    "admin-remove-category": admin_remove_category,
}
