RAFFLE_DB_STATUS_OPEN = "OPEN"
RAFFLE_DB_STATUS_CLOSED = "CLOSED"

# The cost of 1 slot for raffles
RAFFLE_SLOT_COST = 1

# Admin start raffle config
ADMIN_START_RAFFLE_ERROR_RAFFLE_ONGOING = ("Error: There is already an "
                                           "ongoing raffle.")
ADMIN_START_RAFFLE_SUCCESS = ("The raffle for {item_name} with {max_slots} "
                              "slots has been started.")

# Admin end raffle config
ADMIN_END_RAFFLE_ERROR_NO_RAFFLE_ONGOING = "Error: There is no ongoing raffle."
ADMIN_END_RAFFLE_NO_WINNER_NAME = "There is no winner."
ADMIN_END_RAFFLE_SUCCESS = ("The raffle for {item_name} with {max_slots} max "
                            "slots has been closed. The winner is: "
                            "{winner_name}")
ADMIN_END_RAFFLE_PM = "You have won the raffle for {item_name}!"

# Buy slots config
BUY_SLOTS_ERROR_INSUFFICIENT_CREDITS = ("Error: You do not have enough "
                                        "credits (Required: {total_cost}, "
                                        "Owned: {user_credits})")
BUY_SLOTS_ERROR_TOO_MANY_SLOTS = ("Error: There are insufficient slots left "
                                  "to buy (Slots left: {slots_left})")
BUY_SLOTS_SUCCESS = "You have bought {slots} slots"

# Raffle config
RAFFLE_DISPLAY_NO_RAFFLE = """```----- RAFFLE -----
There is currently no raffle.
Try again next time!```"""
RAFFLE_DISPLAY = """```----- RAFFLE -----
Item: {raffle_item}
Used Slots: {current_slots}/{max_slots}
Enter now!!!```"""
