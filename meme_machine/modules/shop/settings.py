# Transaction database config
TRANSACTION_DB_STATUS_PENDING = "PENDING"
TRANSACTION_DB_STATUS_COMPLETE = "COMPLETE"

# Validation config
SHOP_ERROR_NO_SUCH_CATEGORY = "Error: There is no category with that name."

# Shop embed config
SHOP_DISPLAY_EACH_ITEM_NAME = "{stock} x {name} [id: {code_name}]"
SHOP_DISPLAY_EACH_ITEM_VALUE = "{cost}PP"
SHOP_DISPLAY_NO_ITEMS = "No items"

# General shops config
SHOP_ALL_AUTHOR_ICON = "https://i.imgur.com/3Dh1TDW.png"

# Shop embed config
SHOP_TITLE = "Panda Points Shop - {category_code}"

# Shops embed config
SHOPS_TITLE = "Panda Points Shops"
SHOPS_COLOR = 0x000000
SHOPS_VALUE = "Category Code: `{category_code}`"

# Admin set stock config
ADMIN_SET_STOCK_ERROR_NO_SUCH_ITEM = "Error: There is no such item."
ADMIN_SET_STOCK_SUCCESS = "Updated {item_name} stock to {new_stock}"

# Admin update category config
ADMIN_UPDATE_CATEGORY_ERROR_INVALID_TYPE = (
    "Error: The update type is not recognized. It should be one of 'CODE', "
    "'THUMBNAIL_URL', 'NAME' or 'COLOR'.")
ADMIN_UPDATE_CATEGORY_SPACES_NOT_ALLOWED = ("Error: This update type should "
                                            "not have spaces in its values")
ADMIN_UPDATE_CATEGORY_CODE_EXISTS = ("Error: A category with that code "
                                     "already exists")
ADMIN_UPDATE_CATEGORY_SUCCESS = "Updated {update_type} to {update_value}."

# Admin add item config
ADMIN_ADD_ITEM_ERROR_ITEM_ALREADY_EXISTS = ("Error: An item with that name "
                                            "already exists.")
ADMIN_ADD_ITEM_SUCCESS = "Added {stock} {name} to {category_name} for {cost}."

# Admin remove item config
ADMIN_REMOVE_ITEM_ERROR_ITEM_DOES_NOT_EXIST = "Error: The item does not exist."
ADMIN_REMOVE_ITEM_ERROR_ITEM_HAS_PENDING_TRANSACTION = \
    "Error: The item still has pending transactions"
ADMIN_REMOVE_ITEM_SUCCESS = "Removed {name} from {category_name}."
