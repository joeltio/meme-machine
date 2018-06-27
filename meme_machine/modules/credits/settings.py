STARTING_CREDITS = 0

# Credit argument validation constants
CREDIT_ERROR_INVALID_AMOUNT_TYPE = ("Invalid argument type: amount given "
                                    "should be a positive integer.")
# Error for when the range given is incorrect
CREDIT_ERROR_REVERSED_RANGE = ("Error: The upper limit should be larger than "
                               "the lower limit")

# Donate command constants
DONATE_ERROR_SELF_DONATE = "Error: Cannot donate PP to yourself."
DONATE_ERROR_INSUFFICIENT_CREDITS = "Error: You do not have enough credits."
# Requires {amount} and {receiver}
DONATE_SUCCESS = "You have donated {amount}PP to {receiver}!"


# Admin add and remove command constants
# Requires {amount} and {receiver}
ADMIN_ADD_SUCCESS = "You have given {amount}PP to {receiver}"
ADMIN_REMOVE_SUCCESS = "You have removed {amount}PP from {receiver}"

DAILY_CONFIG_MAX_NAME = "daily_max"
DAILY_CONFIG_MIN_NAME = "daily_min"
DAILY_CONFIG_MIN_DEFAULT = 1
DAILY_CONFIG_MAX_DEFAULT = 5
DAILY_SECONDS_LEFT = "You have to wait {seconds} more seconds"
DAILY_MINUTES_LEFT = "You have to wait {minutes} more minutes"
DAILY_HOURS_AND_MINUTES_LEFT = ("You have to wait {hours} hours and {minutes} "
                                "more minutes")
DAILY_SUCCESS = "You have gotten {amount}PP!"

ADMIN_DAILY_AMT_SUCCESS = ("Successfully updated daily range to "
                           "{start}PP-{end}PP")
