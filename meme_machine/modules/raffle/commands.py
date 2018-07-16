from modules.raffle.actions import (admin_start_raffle, admin_end_raffle,
                                    buy_slots, raffle)

COMMANDS = {
    "admin-start-raffle": admin_start_raffle,
    "admin-end-raffle": admin_end_raffle,
    "buy-slots": buy_slots,
    "raffle": raffle,
}
