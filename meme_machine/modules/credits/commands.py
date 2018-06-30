from modules.credits.actions import (donate, admin_add, admin_remove, daily,
                                     admin_daily_amt, admin_randpp_amt,
                                     admin_randpp_time)

COMMANDS = {
    "donate": donate,
    "admin-add": admin_add,
    "admin-remove": admin_remove,
    "daily": daily,
    "admin-daily-amt": admin_daily_amt,
    "admin-randpp-amt": admin_randpp_amt,
    "admin-randpp-time": admin_randpp_time,
}
