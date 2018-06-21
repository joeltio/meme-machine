from modules.credits.commands import COMMANDS as credits_commands, \
                                     COMMAND_AUTH as credits_auth

# Define all the commands and their mapped functions
COMMANDS = {
    **credits_commands
}

COMMAND_AUTH = {
    **credits_auth
}
