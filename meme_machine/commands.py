from modules.credits.commands import COMMANDS as credits_commands
from modules.shop.commands import COMMANDS as shop_commands
from modules.raffle.commands import COMMANDS as raffle_commands

# Define all the commands and their mapped functions
COMMANDS = {
    **credits_commands,
    **shop_commands,
    **raffle_commands,
}
