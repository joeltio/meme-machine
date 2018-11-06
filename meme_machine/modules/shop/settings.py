# Transaction database config
TRANSACTION_DB_STATUS_PENDING = "PENDING"
TRANSACTION_DB_STATUS_SUCCESS = "SUCCESS"
TRANSACTION_DB_STATUS_FAILED = "FAILED"

# Validation config
SHOP_ERROR_NO_SUCH_CATEGORY = "Error: There is no category with that name."
SHOP_ERROR_CATEGORY_EXISTS = "Error: A category with that code already exists"
SHOP_ERROR_CATEGORY_DOES_NOT_EXIST = "Error: The category does not exist."
SHOP_ERROR_ITEM_DOES_NOT_EXIST = "Error: The item does not exist."
SHOP_ERROR_ITEM_EXISTS = ("Error: An item in that category with that code "
                          "already exists")

# Shop embed config
SHOP_DISPLAY_EACH_ITEM_NAME = "{stock} x {name} [id: {code_name}]"
SHOP_DISPLAY_EACH_ITEM_VALUE = "{cost}PP"
SHOP_DISPLAY_NO_ITEMS = "No items"

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
ADMIN_UPDATE_CATEGORY_SUCCESS = "Updated {update_type} to {update_value}."

# Admin add item config
ADMIN_ADD_ITEM_ERROR_ITEM_ALREADY_EXISTS = ("Error: An item with that name "
                                            "already exists.")
ADMIN_ADD_ITEM_SUCCESS = "Added {stock} {name} to {category_name} for {cost}."

# Admin remove item config
ADMIN_REMOVE_ITEM_ERROR_ITEM_HAS_PENDING_TRANSACTION = \
    "Error: The item still has pending transactions"
ADMIN_REMOVE_ITEM_SUCCESS = "Removed {name} from {category_name}."

# Admin update item config
ADMIN_UPDATE_ITEM_ERROR_INVALID_TYPE = (
    "Error: The update type is not recognized. It should be 'COST' OR 'NAME'.")
ADMIN_UPDATE_ITEM_SPACES_NOT_ALLOWED = ("Error: This update type should not "
                                        "have spaces in its values")
ADMIN_UPDATE_ITEM_SUCCESS = "Updated {update_type} to {update_value}"

# Admin add category config
ADMIN_ADD_CATEGORY_SUCCESS = "Added {name} category."

# Admin remove category config
ADMIN_REMOVE_CATEGORY_ERROR_CATEGORY_HAS_ITEMS = ("Error: The category still "
                                                  "has items in it.")
ADMIN_REMOVE_CATEGORY_SUCCESS = "Removed {name} category."

# Buy config
# User id of who receives the purchase order
BUY_PURCHASE_ORDER_DESTINATION = "330241589211299850"
BUY_ERROR_AMOUNT_ZERO = "Error: You cannot buy 0 items."
BUY_ERROR_INSUFFICIENT_CREDITS = ("Error: You do not have enough credits "
                                  "(Required: {total_cost}, Owned: "
                                  "{user_credits})")
BUY_SENDER_SUCCESS = ("Transaction ID: {transaction_id}\n"
                      "Item: {amount}x{item_name}\n"
                      "{total_cost} Panda Points have been deducted from "
                      "your account. Your item should arrive in under "
                      "72 hours.")
BUY_PURCHASE_ORDER_SUCCESS = ("Pending Transaction\n"
                              "ID: {transaction_id}\n"
                              "User: {user_identifier}\n"
                              "PP Spent: {total_cost}\n"
                              "Item: {amount}x{item_name}")

# Transaction config
ADMIN_TRANS_ERROR_DOES_NOT_EXIST = ("Error: The transaction with that id does "
                                    "not exist.")
ADMIN_TRANS_ERROR_STATUS_ALREADY_SET = \
    ("Error: The status for the transaction has already been set to "
     "{current_status}")
ADMIN_TRANS_SUCCESS_INITIATOR = ("Your transaction for {amount}x{item_name} "
                                 "[id: {transaction_id}] has been processed! "
                                 "Check your Steam trades!")
ADMIN_TRANS_FAILED_INITIATOR = ("Your transaction for {amount}x{item_name} "
                                "[id: {transaction_id}] failed. "
                                "{total_cost}PP has been refunded.")
ADMIN_TRANS_SUCCESS = ("The transaction for {amount}x{item_name} [id: "
                       "{transaction_id}] has been set to SUCCESS.")
ADMIN_TRANS_FAILED = ("The transaction for {amount}x{item_name} [id: "
                      "{transaction_id}] has been set to FAILED.")
