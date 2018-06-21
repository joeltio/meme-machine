from modules.credits.actions import donate
from modules.credits.auth import command_auth

COMMANDS = {
    "donate": donate
}

COMMAND_AUTH = {k: command_auth for k in COMMANDS}
