RAFFLE_DB_STATUS_OPEN = "OPEN"
RAFFLE_DB_STATUS_CLOSED = "CLOSED"

# Admin start raffle config
ADMIN_START_RAFFLE_ERROR_RAFFLE_ONGOING = ("Error: There is already an "
                                           "ongoing raffle.")
ADMIN_START_RAFFLE_SUCCESS = ("The raffle for {item_name} with {max_slots} "
                              "slots has been started.")

# Admin end raffle config
ADMIN_END_RAFFLE_ERROR_NO_RAFFLE_ONGOING = "Error: There is no ongoing raffle."
ADMIN_END_RAFFLE_NO_WINNER_NAME = "There is no winner."
ADMIN_END_RAFFLE_SUCCESS = ("The raffle for {item_name} with {max_slots} max "
                            "slots has been closed. The winner is: {winner}")
ADMIN_END_RAFFLE_PM = "You have won the raffle for {item_name}!"
