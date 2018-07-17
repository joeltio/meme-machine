from modules.credits.commands import COMMANDS as credits_commands
from modules.shop.commands import COMMANDS as shop_commands
from modules.raffle.commands import COMMANDS as raffle_commands
from modules.user_info.commands import COMMANDS as user_info_commands

# Define all the commands and their mapped functions
COMMANDS = {
    **credits_commands,
    **shop_commands,
    **raffle_commands,
    **user_info_commands,
}
