import discord

from settings import (BOT_TOKEN, PREFIX, ERROR_NOT_AUTHORISED,
                      ERROR_BAD_PERMISSIONS)
from commands import COMMANDS
from auth import ADMIN_PERMISSIONS, USER_ALLOWED_COMMANDS

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    # Ignore all bot users
    if message.author.bot:
        return

    if message.content.startswith(PREFIX):
        # Remove the prefix from the full command
        full_command = message.content[len(PREFIX):].split()
        # Separate the command from it's arguments
        command = full_command[0]
        arguments = full_command[1:]

        # Ensure that the user is authorized to execute the command
        # The command is a command allowed to all users
        if command in USER_ALLOWED_COMMANDS:
            await COMMANDS[command](client, message, *arguments)
            return

        try:
            # The command requires admin permissions
            # Check if the user is an admin
            if message.author.id not in ADMIN_PERMISSIONS:
                raise Exception(ERROR_NOT_AUTHORISED)

            # Check if the user has the permissions to run the command
            permissions = ADMIN_PERMISSIONS[message.author.id]

            # Command is not in except-commands
            if "except-commands" in permissions:
                if command in permissions["except-commands"]:
                    raise Exception(ERROR_NOT_AUTHORISED)

            # Command is in commands (if there is a commands)
            if "commands" in permissions:
                if command not in permissions["commands"]:
                    raise Exception(ERROR_NOT_AUTHORISED)

            # Extra precaution, ensure that either commands or except-commands
            # is defined. If not, drop to user level permissions and notify the
            # user.
            if "except-commands" not in permissions and \
                    "commands" not in permissions:
                raise Exception(ERROR_BAD_PERMISSIONS)

            await COMMANDS[command](client, message, *arguments)
        except Exception as e:
            await client.send_message(message.channel, e)

client.run(BOT_TOKEN)
