import modules.help.settings as help_settings


async def help(client, message, *args):
    if len(args) > 1:
        error_message = help_settings.HELP_ERROR_WRONG_NUM_ARGS.format(
            given=len(args))
        await client.send_message(message.channel, error_message)
        return
    elif len(args) == 1:
        command = args[0]
        # Remove the ! infront of the command if any
        bare_command = command.lstrip("!")

        if bare_command in help_settings.COMMAND_HELP:
            await client.send_message(
                message.channel, help_settings.COMMAND_HELP[bare_command])
        else:
            await client.send_message(
                message.channel, help_settings.HELP_ERROR_COMMAND_NOT_FOUND)
    else:
        # Show list of commands
        display_message = help_settings.HELP_DISPLAY_TITLE + "\n"

        display_message += "\n".join(help_settings.COMMAND_HELP.keys())

        await client.send_message(message.channel, display_message)
