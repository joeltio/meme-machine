import discord

from settings import BOT_TOKEN, PREFIX
from commands import COMMANDS

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith(PREFIX):
        # Remove the prefix from the full command
        full_command = message.content[len(PREFIX):].split()
        # Separate the command from it's arguments
        command = full_command[0]
        arguments = full_command[1:]
        await COMMANDS[command](client, message, *arguments)

client.run(BOT_TOKEN)
