STARTING_CREDITS = 0

# Credit argument validation constants
CREDIT_ERROR_INVALID_AMOUNT_TYPE = ("Invalid argument type: amount given "
                                    "should be a positive integer.")


# Donate command constants
DONATE_ERROR_SELF_DONATE = "Error: Cannot donate PP to yourself."
DONATE_ERROR_INSUFFICIENT_CREDITS = "Error: You do not have enough credits."
# Requires {amount} and {receiver}
DONATE_SUCCESS = "You have donated {amount}PP to {receiver}!"


# Admin add and remove command constants
# Requires {amount} and {receiver}
ADMIN_ADD_SUCCESS = "You have given {amount}PP to {receiver}"
ADMIN_REMOVE_SUCCESS = "You have removed {amount}PP from {receiver}"
