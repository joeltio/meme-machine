# Specify admin permissions to commands here
# Every user must have either an "except-commands" or "commands" defined. If
# not, they will receive an error and drop to user level permissions
ADMIN_PERMISSIONS = {
    "330241589211299850": {
        "except-commands": []
    },
    "152038584449368064": {
        "except-commands": []
    },
}

# List of all commands allowed to be used by ALL users
USER_ALLOWED_COMMANDS = [
    "donate",
]
