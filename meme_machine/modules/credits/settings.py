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
ADMIN_ADD_SUCCESS = "You have given {amount}PP to {receiver}!"
ADMIN_REMOVE_SUCCESS = "You have removed {amount}PP from {receiver}!"

# Daily config for database retrieval
DAILY_CONFIG_MAX_NAME = "daily_max"
DAILY_CONFIG_MIN_NAME = "daily_min"
DAILY_CONFIG_MIN_DEFAULT = 5
DAILY_CONFIG_MAX_DEFAULT = 15

# Daily command messages
DAILY_SECONDS_LEFT = "You have to wait {seconds} more second(s)."
DAILY_MINUTES_LEFT = "You have to wait {minutes} more minute(s)."
DAILY_HOURS_AND_MINUTES_LEFT = ("You have to wait {hours} hour(s) and "
                                "{minutes} more minute(s).")
DAILY_SUCCESS = "{mention} has just gotten {amount}PP!"

ADMIN_DAILY_AMT_SUCCESS = ("Successfully updated daily range to "
                           "{start}PP-{end}PP.")

# Daily other config
DAILY_INTERVAL_HOURS = 21

# Activeness config for database retrieval
HOOK_USER_ACTIVITY_CONFIG_MIN_TIME_NAME = "user_activity_min_time"
HOOK_USER_ACTIVITY_CONFIG_MAX_TIME_NAME = "user_activity_max_time"
HOOK_USER_ACTIVITY_CONFIG_MIN_AMT_NAME = "user_activity_min_amt"
HOOK_USER_ACTIVITY_CONFIG_MAX_AMT_NAME = "user_activity_max_amt"

HOOK_USER_ACTIVITY_CONFIG_MIN_AMT_DEFAULT = 1
HOOK_USER_ACTIVITY_CONFIG_MAX_AMT_DEFAULT = 5
HOOK_USER_ACTIVITY_CONFIG_MIN_TIME_DEFAULT = 1
HOOK_USER_ACTIVITY_CONFIG_MAX_TIME_DEFAULT = 5

HOOK_USER_ACTIVITY_SUCCESS = "{mention} has just gotten {amount}PP!"

# Admin randpp config messages
ADMIN_RANDPP_AMT_SUCCESS = ("New activeness random PP range set to "
                            "{start}PP-{end}PP.")
ADMIN_RANDPP_TIME_SUCCESS = ("New activeness random time range set to "
                             "{start} minutes - {end} minutes.")
# Admin give rand pp success message
ADMIN_RANDPP_SUCCESS = "You have given {mention} {amount}PP!"
