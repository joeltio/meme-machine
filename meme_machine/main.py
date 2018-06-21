import discord

from settings import BOT_TOKEN, PREFIX
from commands import COMMANDS, COMMAND_AUTH

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
        is_authorized = COMMAND_AUTH[command](message.author, command)
        if is_authorized:
            await COMMANDS[command](client, message, *arguments)
        else:
            await client.send_message(
                message.channel, "You are not allowed to use that command")

client.run(BOT_TOKEN)
