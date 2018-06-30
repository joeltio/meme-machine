from modules.credits.commands import COMMANDS as credits_commands
from modules.shop.commands import COMMANDS as shop_commands

# Define all the commands and their mapped functions
COMMANDS = {
    **credits_commands,
    **shop_commands,
}
