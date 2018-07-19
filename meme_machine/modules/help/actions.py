import modules.help.settings as help_settings


async def help(client, message, command):
    # Remove the ! infront of the command if any
    bare_command = command.lstrip("!")

    if bare_command in help_settings.COMMAND_HELP:
        await client.send_message(
            message.channel, help_settings.COMMAND_HELP[bare_command])
    else:
        await client.send_message(
            message.channel, help_settings.HELP_ERROR_COMMAND_NOT_FOUND)
