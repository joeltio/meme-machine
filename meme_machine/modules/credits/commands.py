from modules.credits.actions import donate, admin_add
from modules.credits.auth import command_auth

COMMANDS = {
    "donate": donate,
    "admin-add": admin_add
}

COMMAND_AUTH = {k: command_auth for k in COMMANDS}
