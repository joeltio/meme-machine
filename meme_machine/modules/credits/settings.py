STARTING_CREDITS = 0

# Donate command constants
DONATE_ERROR_INVALID_AMOUNT_TYPE = ("Invalid argument type: amount given "
                                    "should be a positive integer.")
DONATE_ERROR_SELF_DONATE = "Error: Cannot donate PP to yourself."
DONATE_ERROR_NO_USER_MENTIONED = ("Error: No users were mentioned to receive "
                                  "the PP.")
DONATE_ERROR_TOO_MANY_USERS_MENTIONED = ("Error: Too many users were "
                                         "mentioned to receive the PP.")
DONATE_ERROR_BOT_MENTIONED = "Error: A bot cannot receive PP."
DONATE_ERROR_INSUFFICIENT_CREDITS = "Error: You do not have enough credits."

# Requires {amount} and {receiver}
DONATE_SUCCESS = "You have donated {amount}PP to {receiver}!"


# Admin add command constants
ADMIN_ADD_ERROR_INVALID_AMOUNT_TYPE = ("Invalid argument type: amount given "
                                       "should be a positive integer.")
ADMIN_ADD_ERROR_NO_USER_MENTIONED = ("Error: No users were mentioned to "
                                     "receive the PP.")
ADMIN_ADD_ERROR_TOO_MANY_USERS_MENTIONED = ("Error: Too many users were "
                                            "mentioned to receive the PP.")
ADMIN_ADD_ERROR_BOT_MENTIONED = "Error: A bot cannot receive PP."
ADMIN_ADD_ERROR_INSUFFICIENT_CREDITS = "Error: You do not have enough credits."

# Requires {amount} and {receiver}
ADMIN_ADD_SUCCESS = "You have given {amount}PP to {receiver}"
